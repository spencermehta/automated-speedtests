from django.core.management.base import BaseCommand, CommandError
import speedtest
from autospeed.models import SpeedtestResult
from datetime import datetime


class Command(BaseCommand):
    help = "A description of the command"

    def handle(self, *args, **options):


        servers = []
        # If you want to test against a specific server
        # servers = [1234]

        threads = None
        # If you want to use a single threaded test
        # threads = 1

        s = speedtest.Speedtest()
        s.get_servers(servers)
        s.get_best_server()
        s.download(threads=threads) 
        s.upload(threads=threads)
        results_dict = s.results.dict()

        self.stdout.write("Down: %s" % results_dict) 

        # result = SpeedtestResult(datetime=datetime.now(), download=results_dict['download'], upload=results_dict['upload'], ping=results_dict['ping'])
        result = SpeedtestResult(datetime=results_dict['timestamp'], download=results_dict['download'], upload=results_dict['upload'], ping=results_dict['ping'])
        result.save()