import speedtest

servers = []
# If you want to test against a specific server
# servers = [1234]

threads = None
# If you want to use a single threaded test
# threads = 1

s = speedtest.Speedtest()
s.get_servers(servers)
s.get_best_server()
print(s.download(threads=threads) / 1024 / 1024)
print(s.upload(threads=threads) / 1024 / 1024)
s.results.share()

results_dict = s.results.dict()