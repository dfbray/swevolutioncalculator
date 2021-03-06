#Most of this code is from the https://github.com/astrofrog/psrecord source. We had to change it slightly for our use cases,
#and because we could not get it to run correctly on Windows through command line. All credit goes to the Github link above.

from __future__ import (unicode_literals, division, print_function,
                        absolute_import)

#import unicode_literals
#import division
#import print_function
#import absolute_import

import psutil
import sys

import time
import argparse

children = []
global child_pid
child_pid = 0

def get_percent(process):
    return (process.cpu_percent() / psutil.cpu_count())


def get_memory(process):
    return process.memory_info()


def all_children(pr):

    global children
    global child_pid

    try:
        children_of_pr = pr.children(recursive=True)
#        print("children", children_of_pr)
#        print("child", children_of_pr[0].pid)
        child_pid = children_of_pr[0].pid
    except Exception:  # pragma: no cover
        return children

    for child in children_of_pr:
        if child not in children:
            children.append(child)

    return children

#def monitor(pid, logfile=None, plot=True, duration=60, interval=1,
#            include_children=False):

pid = sys.argv[1]
forbidden_pid = sys.argv[2]
#print('in python', pid)
pid = int(pid)
forbidden_pid = int(forbidden_pid)
#print("forbidden pid", forbidden_pid)
interval = .1
include_children=True
plot=True
logfile=True

    # We import psutil here so that the module can be imported even if psutil
    # is not present (for example if accessing the version)
    #import psutil

pr = psutil.Process(pid)
if(forbidden_pid != 0):
    forbidden = psutil.Process(forbidden_pid)

    # Record start time
start_time = time.time()

if logfile:
    f = open("log.txt", 'w')
    f.write("# {0:12s} {1:12s} {2:12s} {3:12s}\n".format(
        'Elapsed time'.center(12),
        'CPU (%)'.center(12),
        'Real (MB)'.center(12),
        'Virtual (MB)'.center(12))
    )

log = {}
log['times'] = [0]
log['cpu'] = [0]
log['mem_real'] = [0]
log['mem_virtual'] = [0]

count = 0

try:

    # Start main event loop
    while(pid in psutil.pids()):

        # Find current time
        current_time = time.time()

        try:
            pr_status = pr.status()
        except TypeError:  # psutil < 2.0
            pr_status = pr.status
        except psutil.NoSuchProcess:  # pragma: no cover
            break

        # Check if process status indicates we should exit
        if pr_status in [psutil.STATUS_ZOMBIE, psutil.STATUS_DEAD]:
            print("Process finished ({0:.2f} seconds)".format(current_time - start_time))
            break

            # Check if we have reached the maximum time
        #if duration is not None and current_time - start_time > duration:
        #    break

        # Get current CPU and memory
        try:
            current_cpu = get_percent(pr)
            current_mem = get_memory(pr)
            if(forbidden_pid != 0):
                current_cpu += get_percent(forbidden)
                current_mem2 = get_memory(forbidden)
        except Exception:
            break
        current_mem_real = current_mem.rss / 1024. ** 2
        current_mem_virtual = current_mem.vms / 1024. ** 2

        if(forbidden_pid != 0):
            current_mem_real += current_mem2.rss / 1024. ** 2
            current_mem_virtual += current_mem2.vms / 1024. ** 2

        # Get information for children
        if include_children:
            for child in all_children(pr):
                try:
                    current_cpu += get_percent(child)
                    current_mem = get_memory(child)
                except Exception:
                    continue
                current_mem_real += current_mem.rss / 1024. ** 2
                current_mem_virtual += current_mem.vms / 1024. ** 2

        if logfile:
            f.write("{0:12.3f} {1:12.3f} {2:12.3f} {3:12.3f}\n".format(
                current_time - start_time,
                current_cpu,
                current_mem_real,
                current_mem_virtual))
            f.flush()

        if interval is not None:
            time.sleep(interval)

        # If plotting, record the values
        if plot:
            log['times'].append(current_time - start_time)
            log['cpu'].append(current_cpu)
            log['mem_real'].append(current_mem_real)
            log['mem_virtual'].append(current_mem_virtual)

    count+=interval

except KeyboardInterrupt:  # pragma: no cover
    pass

if logfile:
    f.close()

if plot:

    # Use non-interactive backend, to enable operation on headless machines
    import matplotlib.pyplot as plt
    with plt.rc_context({'backend': 'Agg'}):

        fig = plt.figure()
        ax = fig.add_subplot(1, 1, 1)

        cpu = ax.plot(log['times'], log['cpu'], '-', lw=1, color='r', label='Average CPU Usage Per Core')

        ax.set_ylabel('CPU (%)')
        ax.set_xlabel('time (s)')
        ax.set_ylim(0., max(log['cpu']) * 1.2)

        ax2 = ax.twinx()

        real = ax2.plot(log['times'], log['mem_real'], '-', lw=1, color='b', label='Real Memory')
        virtual = ax2.plot(log['times'], log['mem_virtual'], '-', lw=1, color='g', label='Virtual Memory')
        ax2.set_ylim(0., max(log['mem_virtual']) * 1.2)
        ax2.set_ylabel('Memory (MB)')

        lns = cpu+real+virtual
        labs = [l.get_label() for l in lns]
        ax.legend(lns, labs, loc=0)

        ax.grid()

        fig.savefig('img.png')

f = open("../../pid.txt", "w")
f.write(str(child_pid))
f.close()

#print('EXITING')
#print(child_pid)

sys.exit(child_pid)

#TODO psrecord $(ps | grep chrome | tr -s ' ' | cut -d ' ' -f 7) --interval 1 --plot plot1.png
#TODO Change code to check for PID itself, and to run on a while(PID exists) loop
#monitor(3300)
