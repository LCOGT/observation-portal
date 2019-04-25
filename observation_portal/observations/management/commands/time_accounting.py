from django.core.management.base import BaseCommand
from datetime import datetime, timedelta
from observation_portal.common.configdb import configdb
from observation_portal.observations.models import Observation
from observation_portal.proposals.models import Proposal, Semester, TimeAllocation


class Command(BaseCommand):
    help = 'Performs time accounting on a specific proposal and instrument type and semester'

    def add_arguments(self, parser):
        proposals = [p['id'] for p in Proposal.objects.all().values('id')]
        parser.add_argument('-p', '--proposal', type=str, choices=proposals, default='',
                            help='Proposal id to perform time accounting on. Default empty string for all proposals.')
        instrument_types = [it[0] for it in configdb.get_instrument_type_tuples()]
        parser.add_argument('-i', '--instrument_type', type=str, choices=instrument_types, default='',
                            help='Instrument type to perform time accounting on. Default empty string for all types.')
        semesters = [s['id'] for s in Semester.objects.all().values('id')]
        current_semester = Semester.current_semesters().first()
        parser.add_argument('-s', '--semester', type=str, choices=semesters, default=current_semester.id,
                            help='Semester to perform time accounting on. Defaults to current semester.')
        parser.add_argument('-d', '--dry-run', dest='dry_run', action='store_true', default=False,
                            help='Dry-run mode will print the time totals but not change anything in the db.')

    def handle(self, *args, **options):
        proposal_str = options['proposal'] or 'All'
        instrument_type_str = options['instrument_type'] or 'All'
        semester_str = options['semester']
        dry_run_str = 'Dry Run Mode: ' if options['dry_run'] else ''
        print(
            f"{dry_run_str}Running time accounting for Proposal(s): {proposal_str} and Instrument Type(s): {instrument_type_str} in Semester: {semester_str}")

        if options['proposal']:
            proposals = [Proposal.objects.get(id=options['proposal'])]
        else:
            proposals = Proposal.objects.all(active=True)

        if options['instrument_type']:
            instrument_types = [options['instrument_type'].upper()]
        else:
            instrument_types = [it[0].upper() for it in configdb.get_instrument_type_tuples()]

        semester = Semester.objects.get(id=options['semester'])
        for proposal in proposals:
            for instrument_type in instrument_types:
                attempted_time = {
                    'NORMAL': 0,
                    'RAPID_RESPONSE': 0,
                    'TIME_CRITICAL': 0
                }
                observations = Observation.objects.filter(end__gt=semester.start, start__lt=semester.end,
                                                          request__request_group__proposal=proposal.id,
                                                          request__configurations__instrument_type=instrument_type,
                                                          ).exclude(state='PENDING').prefetch_related(
                    'request, '
                    'request__request_group',
                    'configuration_statuses',
                    'configuration_statuses__summary'
                )
                for observation in observations:
                    observation_type = observation.request.request_group.observation_type
                    configuration_time = timedelta(seconds=0)
                    for configuration_status in observation.configuration_statuses.all():
                        if configuration_status.hasattr('summary'):
                            configuration_time += configuration_status.summary.end - configuration_status.summary.start
                    block_time = observation.end - observation.start
                    if observation_type == 'RAPID_RESPONSE' and block_time < configuration_time:
                        configuration_time = block_time
                    attempted_time[observation_type] += configuration_time

                print(
                    "Proposal: {}, Instrument Type: {}, Used {} NORMAL hours, {} RAPID_RESPONSE hours, and {} TIME_CRITICAL hours".format(
                        proposal.id, instrument_type, attempted_time['NORMAL'], attempted_time['RAPID_RESPONSE'],
                        attempted_time['TIME_CRITICAL']
                    ))
                if not options['dry_run']:
                    # Update the time allocation for this proposal accordingly
                    time_allocation = TimeAllocation.objects.get(proposal=proposal, instrument_type=instrument_type,
                                                                 semester=semester)
                    time_allocation.std_time_used = attempted_time['NORMAL']
                    time_allocation.rr_time_used = attempted_time['RAPID_RESPONSE']
                    time_allocation.tc_time_used = attempted_time['TIME_CRITICAL']
                    time_allocation.save()
