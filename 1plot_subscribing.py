from matplotlib.pyplot import plot, annotate, legend, savefig
from matplotlib.pyplot import xlim, ylim, xlabel, ylabel, subplots_adjust
from matplotlib import rc, rcParams
from csv import reader
from itertools import islice


def fix_start(time_list, bytes_list):
    time_list.insert(0, 0)
    bytes_list.insert(0, 0)
    time_list.insert(1, time_list[1])
    bytes_list.insert(0, 0)


def fix_start_end(time_list, bytes_list, ending_list):
    time_list.insert(0, 0)
    bytes_list.insert(0, 0)
    time_list.insert(1, time_list[1])
    bytes_list.insert(0, 0)
    time_list.append(time_list[-1])
    bytes_list.append(0)
    time_list.append(ending_list[-1])
    bytes_list.append(0)


# rcParams['font.family'] = 'Times New Roman'
rcParams['font.size'] = '20'
rcParams['figure.figsize'] = [20, 5]
subplots_adjust(left=.06, bottom=.14, right=.98, top=.97)
rc('savefig', dpi=300, format='png')
rc('axes', autolimit_mode='round_numbers', xmargin=0, ymargin=0)
ylim(top=1.5)
xlim(1.5, 20)
xlabel('Time(s)')
ylabel('KBytes/s')
# tshark -r logs/pcap/ied2.pcap -T fields -e frame.time_epoch -e frame.len \
# -e _ws.col.Protocol -E header=y -E separator=, -E quote=d > logs/ied2.csv

time_ied1, kbytes_ied1 = [], []
time_ied2, kbytes_ied2 = [], []
time_auth, kbytes_auth = [], []
time_abac, kbytes_abac = [], []
start_time = None

with open('experiment1/logs/ied1.csv') as csv_file:
    ied1 = reader(csv_file, delimiter=',')

    for row in islice(ied1, 1, None):  # skip header
        if row[2] != 'GOOSE':
            # start_time = None
            time_ied1 = []
            kbytes_ied1 = []
        else:
            if not start_time:
                start_time = float(row[0]) + 2.1
            time = float(row[0]) - start_time
            if (time) <= 20:
                kbytes = int(row[1]) / 1024
                time_ied1.append(time)
                kbytes_ied1.append(kbytes)

with open('experiment1/logs/ied2.csv') as csv_file:
    ied2 = reader(csv_file, delimiter=',')

    for row in islice(ied2, 1, None):  # skip header
        time = float(row[0]) - start_time
        if (time) <= 20:
            kbytes = int(row[1]) / 1024
            if row[2] == 'GOOSE':
                time_ied2.append(time)
                kbytes_ied2.append(kbytes)
            elif row[2] in ('TCP', 'COTP', 'MMS', 'ACSE'):
                time_abac.append(time)
                kbytes_abac.append(kbytes)
            else:
                time_auth.append(time)
                kbytes_auth.append(kbytes)

fix_start(time_ied1, kbytes_ied1)
fix_start(time_ied2, kbytes_ied2)
fix_start_end(time_auth, kbytes_auth, time_ied1)
fix_start_end(time_abac, kbytes_abac, time_ied1)

plot(
    time_ied1, kbytes_ied1, linestyle='--', marker=None,
    label='GOOSE sendo publicado pelo IED1 autorizado')
plot(
    time_auth, kbytes_auth, linestyle='-', marker='x',
    label='Autenticação IEEE 802.1X pelo IED2')
plot(
    time_abac, kbytes_abac, linestyle='-', marker='+',
    label='Processo de autorização por MMS do IED2')
plot(
    time_ied2, kbytes_ied2, linestyle='-', marker=None,
    label='GOOSE sendo recebido pelo IED2')

annotate(
    'IED2 é autorizado', xy=(11.05, .25), xytext=(9, .6),
    bbox=dict(boxstyle="round4", fc="w", facecolor='gray'),
    arrowprops=dict(facecolor='gray', arrowstyle='->'),
)

annotate(
    'IED2 começa a receber GOOSE', xy=(11.4, .25), xytext=(11, .4),
    bbox=dict(boxstyle="round4", fc="w", facecolor='gray'),
    arrowprops=dict(facecolor='gray', arrowstyle='->'),
)

legend()
savefig('experiment1/subscribing.png')
