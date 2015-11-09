# Joseph DeBruycker
# -01213128
# CSCI 460
# Assignment 1:  Processor Scheduling
# Fall 2015
#
# This python module simulates a 4 core non-preemptive process scheduler.  It simulates a round-robin
# procedure of assigning jobs to each core and has options to run random job sequences of 1000 jobs
# that have processing times between 1 and 500 or to run a set sequence of 12 jobs as defined in class.
# The module also contains a procedure designed to beat the round robin scheduler, which watches the
# cores' total queued processing time (since this value is known for this exercise), and assigns each
# new job to the core with the lowest processing time(service time) remaining.

import random
import statistics
from queue import Queue


# Create a scheduler object which uses either Round Robin scheduling(param 0) or an improved scheduling(param 1).  The scheduler
# has methods to add jobs to the job list, assign jobs to its 4 cores, process all jobs on all cores for 1 millisecond, run
# the scheduler, and report the clock time.
class Scheduler:
    
    def __init__(self, scheduler_type = 0):
        self.clock = 0
        self.core0 = Core()
        self.core1 = Core()
        self.core2 = Core()
        self.core3 = Core()
        self.job_list = Queue()
        self.scheduler = scheduler_type
        self.next_processor = 0
        self.first_arrival_time = -1
        
    def add_job(self, processing_time, arrival_time = 0):
        self.job_list.put(Job(processing_time, arrival_time))
        
    def assign_job(self, my_job):
        # Remember first arrival time to calculate overall turnaround time
        if(self.first_arrival_time == -1):
            self.first_arrival_time = my_job.peek_arrival_time()
        # Round Robin Method
        if(self.scheduler == 0):
            # Core 0
            if(self.next_processor == 0):
                self.core0.assign_job(my_job)
                self.next_processor += 1
            # Core 1
            elif(self.next_processor == 1):
                self.core1.assign_job(my_job)
                self.next_processor += 1   
            # Core 2 
            elif(self.next_processor == 2):
                self.core2.assign_job(my_job)
                self.next_processor += 1
            # Core 3
            else:
                self.core3.assign_job(my_job)
                self.next_processor = 0
        # Improved Method
        elif(self.scheduler == 1):
            # Update the total time in each processor job queue
            c0 = self.core0.peek_queue_proc_time()
            c1 = self.core1.peek_queue_proc_time()
            c2 = self.core2.peek_queue_proc_time()
            c3 = self.core3.peek_queue_proc_time()
            # Assign job to the core with lowest queue time
            if(c0 <= c1 and c0 <= c2 and c0 <= c3):
                self.core0.assign_job(my_job)
            elif(c1 <= c0 and c1 <= c2 and c1 <= c3):
                self.core1.assign_job(my_job)
            elif(c2 <= c0 and c2 <= c1 and c2 <= c3):
                self.core2.assign_job(my_job)
            else:
                self.core3.assign_job(my_job)
            
                
    def process_jobs(self):
        self.clock += 1
        self.core0.process_job()
        self.core1.process_job()
        self.core2.process_job()
        self.core3.process_job()
                         
    def tick(self):
        # assign all jobs in the job list
        while(not self.job_list.empty()):
            next_job = self.job_list.get()
            # account for arrival times in jobs where they are specified
            while (next_job.has_not_arrived(self.clock)):
                self.process_jobs()
            # assign the current job
            self.assign_job(next_job)
            self.process_jobs()
        # finish processing jobs after all jobs have been assigned
        while(self.core0.is_busy() or self.core1.is_busy() or self.core2.is_busy() or self.core3.is_busy()):
            self.process_jobs()
            
    def report_turnaround_time(self):
        return self.clock - self.first_arrival_time
    
            
class Core:
    
    def __init__(self):
        self.jobs = Queue()
        self.busy = False
        self.queued_proc_time = 0
        
    def is_busy(self):
        return self.busy
    
    def assign_job(self, new_job):
        self.jobs.put(new_job)
        self.queued_proc_time += new_job.peek_processing_time()
        
    def process_job(self):
        if(self.is_busy()):
            self.current_job.process()
            self.queued_proc_time -= 1
            if(self.current_job.is_finished()):
                self.busy = False
        elif(not self.jobs.empty()):
            self.current_job = self.jobs.get()
            self.current_job.process()
            self.queued_proc_time -= 1
            if(self.current_job.is_finished()):
                self.busy = False
            else:
                self.busy = True
        else:
            self.busy = False
            
    def peek_queue_proc_time(self):
        return self.queued_proc_time
        
    
class Job:
    
    def __init__(self, p_time, a_time = 0):
        # Service time is processing time + 1 ms to put job on processor
        self.service_time = p_time + 1
        self.execution_time = 0
        self.arrival_time = a_time
        
    def has_not_arrived(self, current_clock):
        if(self.arrival_time == 0):
            return False
        elif(self.arrival_time == current_clock):
            return False
        else:
            return True        
        
    def is_finished(self):
        if(self.service_time == self.execution_time):
            return True
        else:
            return False
        
    def process(self):
        self.execution_time += 1
        
    def peek_arrival_time(self):
        return self.arrival_time
    
    def peek_processing_time(self):
        return self.service_time - 1
        

# Main program control loop        
if __name__ == "__main__":
    finished = False
    while(not finished):
        print("Welcome to the 4 core processor scheduler simulator!\n")
        print("Would you like to run the round robin scheduler or the improved scheduler?")
        print("1.  Round Robin")
        print("2.  Improved")
        try:
            scheduler = int(input("(Enter selection (1 or 2): "))
            if(scheduler > 2 or scheduler < 1):
                print("Invalid selection, running Round Robin")
                scheduler = 1
        except ValueError:
            print("Invalid selection, running Round Robin")
            scheduler = 1
        if(scheduler == 1):
            print("Using Round Robin")
            scheduler_type = 0
        if(scheduler == 2):
            print("Using Improved")
            scheduler_type = 1
        print("Would you like to run the preprogrammed job list or a random job list?")
        print("1. Preprogrammed")
        print("2. Random")
        try:
            job_list = int(input("(Enter selection (1 or 2): "))
            if(job_list > 2 or job_list < 1):
                print("Invalid selection, running Preprogrammed")
                job_list = 1
        except ValueError:
            print("Invalid selection, running Preprogrammed")
            job_list = 1  
        # Preprogrammed job list 
        if(job_list == 1):
            print("Running pre-programmed job list...")
            MyScheduler = Scheduler(scheduler_type)
            MyScheduler.add_job(9, 4)
            MyScheduler.add_job(2, 15)
            MyScheduler.add_job(16, 18)
            MyScheduler.add_job(3, 20)
            MyScheduler.add_job(29, 26)
            MyScheduler.add_job(198, 29)
            MyScheduler.add_job(7, 35)
            MyScheduler.add_job(170, 45)
            MyScheduler.add_job(180, 57)
            MyScheduler.add_job(178, 83)
            MyScheduler.add_job(73, 88)
            MyScheduler.add_job(8, 95)
            MyScheduler.tick()
            tat = MyScheduler.report_turnaround_time()
            print("Overall turnaround time: ", tat, "ms")
        # Random Job List
        else:
            print("Running 100 instances of 1000 random jobs...")
            max_tat = 0
            min_tat = 1000000
            # Array for collecting each turn-around time
            tats = []
            for i in range (0,100):
                MyScheduler = Scheduler(scheduler_type)
                # Add 1000 random jobs
                for j in range(0,1000):
                    MyScheduler.add_job(random.randint(1,500))
                MyScheduler.tick()
                tat = MyScheduler.report_turnaround_time()
                if(tat > max_tat):
                    max_tat = tat
                if(tat < min_tat):
                    min_tat = tat
                tats.append(tat)
            print("Minimum turnaround time: ", min_tat, "ms")
            print("Maximum turnaround time: ", max_tat, "ms")
            print("Average turnaround time: ", statistics.mean(tats), "ms")
            print("Std Deviation of turnaround times: ", statistics.stdev(tats), "ms")
        print("All done?")
        try:
            selection = int(input("Press 1 to quit or any other key to start over: "))
        except ValueError:
            selection = 0
        if(selection == 1):
            finished = True
        
        
            