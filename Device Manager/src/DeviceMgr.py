# Joseph DeBruycker
# -01213128
# CSCI 460
# Assignment 3
# Fall 2015
#

import random
import statistics
from collections import deque


class DeviceMgr:
    
    def __init__(self):
        self.requests = []
        self.fcfs_tat = 0
        self.sstf_tat = 0
        self.look_tat = 0
        self.clook_tat = 0
        self.num_requests = 0
        
    def add_request(self, myRequest):
        self.requests.append(myRequest)
        self.num_requests += 1
        
    def sort_requests(self):
        self.requests.sort(key = lambda request: request.arrival)
        
    def sector_time(self, current_s, requested_s):
        if(current_s <= requested_s):
            return requested_s - current_s
        else:
            return (8-current_s) + requested_s
            
        
    def run_fcfs(self):
        current_track = 0
        current_sector = 0
        clock = 0
        my_requests = deque()
        tats = []
        
        for req in self.requests:
            my_requests.append(req)
            
        for i in range (0, self.num_requests):
            r = my_requests.popleft()
            if(r.arrival > clock):
                clock = r.arrival
            finish_time = clock + 11 + (0.1 * abs(current_track-r.track)) + self.sector_time(current_sector, r.sector)
            tat = round(finish_time - r.arrival, 1)
            tats.append(tat)
            clock = finish_time
            current_sector = r.sector
            current_track = r.track
            
        self.fcfs_mean = statistics.mean(tats)
        self.fcfs_variance = statistics.variance(tats)
        self.fcfs_stdev = statistics.stdev(tats)
        
    def run_sstf(self):
        current_track = 0
        current_sector = 0
        clock = 0
        my_requests = deque()
        arrived_requests = deque()
        tats = []
        
        for req in self.requests:
            my_requests.append(req)
            
        while my_requests:
            r = my_requests.popleft()
            if(r.arrival > clock):
                clock = r.arrival
            my_requests.appendleft(r)
            
            arriving = True
            while(arriving):
                if(my_requests):
                    r = my_requests.popleft()
                    if(r.arrival > clock):
                        my_requests.appendleft(r)
                        arriving = False
                    else:
                        arrived_requests.append(r) 
                else:
                    arriving = False          
            
            nextreq = arrived_requests.popleft()
            for i in range(0, len(arrived_requests)):
                check = arrived_requests.popleft()
                if(abs(check.track - current_track) < abs(nextreq.track - current_track)):
                    arrived_requests.append(nextreq)
                    nextreq = check
                else:
                    arrived_requests.append(check)
                         
            finish_time = clock + 11 + (0.1 * abs(current_track-nextreq.track)) + self.sector_time(current_sector, nextreq.sector)
            tat = round(finish_time - nextreq.arrival, 1)
            tats.append(tat)
            clock = finish_time
            current_sector = nextreq.sector
            current_track = nextreq.track
            
        while(arrived_requests):
            nextreq = arrived_requests.popleft()
            for i in range(0, len(arrived_requests)):
                check = arrived_requests.popleft()
                if(abs(check.track - current_track) < abs(nextreq.track - current_track)):
                    arrived_requests.append(nextreq)
                    nextreq = check
                else:
                    arrived_requests.append(check)
                         
            finish_time = clock + 11 + (0.1 * abs(current_track-nextreq.track)) + self.sector_time(current_sector, nextreq.sector)
            tat = round(finish_time - nextreq.arrival, 1)
            tats.append(tat)
            clock = finish_time
            current_sector = nextreq.sector
            current_track = nextreq.track
            
        self.sstf_mean = statistics.mean(tats)
        self.sstf_variance = statistics.variance(tats)
        self.sstf_stdev = statistics.stdev(tats)
        
    def run_look(self):
        current_track = 0
        current_sector = 0
        clock = 0
        ascending = True
        my_requests = deque()
        arrived_asc = deque()
        arrived_desc = deque()
        tats = []
        
        for req in self.requests:
            my_requests.append(req)
            
        while my_requests:
            r = my_requests.popleft()
            if(r.arrival > clock):
                clock = r.arrival
            my_requests.appendleft(r)
            
            arriving = True
            while(arriving):
                if(my_requests):
                    r = my_requests.popleft()
                    if(r.arrival > clock):
                        my_requests.appendleft(r)
                        arriving = False
                    else:
                        if(ascending):
                            if((r.track - current_track)<0):
                                arrived_desc.append(r)
                            else:
                                arrived_asc.append(r)
                        else:
                            if((r.track - current_track)>0):
                                arrived_asc.append(r)
                            else:
                                arrived_desc.append(r)
                else:
                    arriving = False  
                    
            if(ascending):
                if(arrived_asc):
                    nextreq = arrived_asc.popleft()
                    for i in range(0, len(arrived_asc)):
                        check = arrived_asc.popleft()
                        if(abs(check.track - current_track) < abs(nextreq.track - current_track)):
                            arrived_asc.append(nextreq)
                            nextreq = check
                        else:
                            arrived_asc.append(check)
                    
                    finish_time = clock + 11 + (0.1 * abs(current_track-nextreq.track)) + self.sector_time(current_sector, nextreq.sector)
                    tat = round(finish_time - nextreq.arrival, 1)
                    tats.append(tat)
                    clock = finish_time
                    current_sector = nextreq.sector
                    current_track = nextreq.track        
                else:
                    ascending = False;
            else:
                if(arrived_desc):
                    nextreq = arrived_desc.popleft()
                    for i in range(0, len(arrived_desc)):
                        check = arrived_desc.popleft()
                        if(abs(check.track - current_track) < abs(nextreq.track - current_track)):
                            arrived_desc.append(nextreq)
                            nextreq = check
                        else:
                            arrived_desc.append(check)
                    
                    finish_time = clock + 11 + (0.1 * abs(current_track-nextreq.track)) + self.sector_time(current_sector, nextreq.sector)
                    tat = round(finish_time - nextreq.arrival, 1)
                    tats.append(tat)
                    clock = finish_time
                    current_sector = nextreq.sector
                    current_track = nextreq.track
                else:
                    ascending = True;
                    
        while(arrived_asc or arrived_desc):
            if(ascending):
                if(arrived_asc):
                    nextreq = arrived_asc.popleft()
                    for i in range(0, len(arrived_asc)):
                        check = arrived_asc.popleft()
                        if(abs(check.track - current_track) < abs(nextreq.track - current_track)):
                            arrived_asc.append(nextreq)
                            nextreq = check
                        else:
                            arrived_asc.append(check)
                    
                    finish_time = clock + 11 + (0.1 * abs(current_track-nextreq.track)) + self.sector_time(current_sector, nextreq.sector)
                    tat = round(finish_time - nextreq.arrival, 1)
                    tats.append(tat)
                    clock = finish_time
                    current_sector = nextreq.sector
                    current_track = nextreq.track        
                else:
                    ascending = False;
            else:
                if(arrived_desc):
                    nextreq = arrived_desc.popleft()
                    for i in range(0, len(arrived_desc)):
                        check = arrived_desc.popleft()
                        if(abs(check.track - current_track) < abs(nextreq.track - current_track)):
                            arrived_desc.append(nextreq)
                            nextreq = check
                        else:
                            arrived_desc.append(check)
                    
                    finish_time = clock + 11 + (0.1 * abs(current_track-nextreq.track)) + self.sector_time(current_sector, nextreq.sector)
                    tat = round(finish_time - nextreq.arrival, 1)
                    tats.append(tat)
                    clock = finish_time
                    current_sector = nextreq.sector
                    current_track = nextreq.track
                else:
                    ascending = True;
                         
        self.look_mean = statistics.mean(tats)
        self.look_variance = statistics.variance(tats)
        self.look_stdev = statistics.stdev(tats)
        
    def run_clook(self):
        current_track = 0
        current_sector = 0
        clock = 0
        my_requests = deque()
        arrived_current = deque()
        arrived_next = deque()
        tats = []
        
        for req in self.requests:
            my_requests.append(req)
            
        while my_requests:
            r = my_requests.popleft()
            if(r.arrival > clock):
                clock = r.arrival
            my_requests.appendleft(r)
            
            arriving = True
            while(arriving):
                if(my_requests):
                    r = my_requests.popleft()
                    if(r.arrival > clock):
                        my_requests.appendleft(r)
                        arriving = False
                    else:
                        if((r.track - current_track)<0):
                            arrived_next.append(r)
                        else:
                            arrived_current.append(r)
                else:
                    arriving = False  

            if(arrived_current):
                nextreq = arrived_current.popleft()
                for i in range(0, len(arrived_current)):
                    check = arrived_current.popleft()
                    if(abs(check.track - current_track) < abs(nextreq.track - current_track)):
                        arrived_current.append(nextreq)
                        nextreq = check
                    else:
                        arrived_current.append(check)
                    
                finish_time = clock + 11 + (0.1 * abs(current_track-nextreq.track)) + self.sector_time(current_sector, nextreq.sector)
                tat = round(finish_time - nextreq.arrival, 1)
                tats.append(tat)
                clock = finish_time
                current_sector = nextreq.sector
                current_track = nextreq.track        
            elif(arrived_next):
                for r in arrived_next:
                    arrived_current.append(r)
                arrived_next.clear()
                nextreq = arrived_current.popleft()
                for i in range(0, len(arrived_current)):
                    check = arrived_current.popleft()
                    if(abs(check.track - current_track) > abs(nextreq.track - current_track)):
                        arrived_current.append(nextreq)
                        nextreq = check
                    else:
                        arrived_current.append(check)
                    
                finish_time = clock + 11 + (0.1 * abs(current_track-nextreq.track)) + self.sector_time(current_sector, nextreq.sector)
                tat = round(finish_time - nextreq.arrival, 1)
                tats.append(tat)
                clock = finish_time
                current_sector = nextreq.sector
                current_track = nextreq.track        
                    
        while(arrived_current or arrived_next):
            if(arrived_current):
                nextreq = arrived_current.popleft()
                for i in range(0, len(arrived_current)):
                    check = arrived_current.popleft()
                    if(abs(check.track - current_track) < abs(nextreq.track - current_track)):
                        arrived_current.append(nextreq)
                        nextreq = check
                    else:
                        arrived_current.append(check)
                    
                finish_time = clock + 11 + (0.1 * abs(current_track-nextreq.track)) + self.sector_time(current_sector, nextreq.sector)
                tat = round(finish_time - nextreq.arrival, 1)
                tats.append(tat)
                clock = finish_time
                current_sector = nextreq.sector
                current_track = nextreq.track        
            elif(arrived_next):
                for r in arrived_next:
                    arrived_current.append(r)
                arrived_next.clear()
                nextreq = arrived_current.popleft()
                for i in range(0, len(arrived_current)):
                    check = arrived_current.popleft()
                    if(abs(check.track - current_track) > abs(nextreq.track - current_track)):
                        arrived_current.append(nextreq)
                        nextreq = check
                    else:
                        arrived_current.append(check)
                    
                finish_time = clock + 11 + (0.1 * abs(current_track-nextreq.track)) + self.sector_time(current_sector, nextreq.sector)
                tat = round(finish_time - nextreq.arrival, 1)
                tats.append(tat)
                clock = finish_time
                current_sector = nextreq.sector
                current_track = nextreq.track
            
        self.clook_mean = statistics.mean(tats)
        self.clook_variance = statistics.variance(tats)
        self.clook_stdev = statistics.stdev(tats)
        
class Request:
    
    def __init__(self, a, t, s):
        self.arrival = a
        self.track = t
        self.sector = s
        
    def __repr__(self):
        return repr((self.arrival, self.track, self.sector))
        

# Main program control loop        
if __name__ == "__main__":
    dmgr = DeviceMgr()
    dmgr.add_request(Request(0,54,0))
    dmgr.add_request(Request(23, 132, 6))
    dmgr.add_request(Request(26, 29, 2))
    dmgr.add_request(Request(29, 23, 1))
    dmgr.add_request(Request(35, 198, 7))
    dmgr.add_request(Request(45, 170, 5))
    dmgr.add_request(Request(57, 180, 3))
    dmgr.add_request(Request(83, 78, 4))
    dmgr.add_request(Request(88, 73, 5))
    dmgr.add_request(Request(95, 249, 7))
    
    dmgr.run_fcfs()
    dmgr.run_sstf()
    dmgr.run_look()
    dmgr.run_clook()
    
    print("Test Data Results:")
    print("Strategy:    Average TAT:    StDev:    Variance:")
    print(" FCFS        ", dmgr.fcfs_mean, "         ", round(dmgr.fcfs_stdev,2), "   ", round(dmgr.fcfs_variance, 2))
    print(" SSTF        ", dmgr.sstf_mean, "         ", round(dmgr.sstf_stdev,2), "   ", round(dmgr.sstf_variance, 2))
    print(" LOOK        ", dmgr.look_mean, "         ", round(dmgr.look_stdev,2), "   ", round(dmgr.look_variance, 2))
    print(" CLOOK       ", dmgr.clook_mean, "         ", round(dmgr.clook_stdev,2), "   ", round(dmgr.clook_variance, 2))
    
    rndmgr = DeviceMgr()
    for i in range(0,50):
        rndmgr.add_request(Request(random.randint(0,99), random.randint(0,249), random.randint(0,7)))
        
    rndmgr.sort_requests()
        
    rndmgr.run_fcfs()
    rndmgr.run_sstf()
    rndmgr.run_look()
    rndmgr.run_clook()
    
    print("")
    print("Random Data Results:")
    print("Strategy:    Average TAT:    StDev:    Variance:")
    print(" FCFS        ", round(rndmgr.fcfs_mean, 2), "         ", round(rndmgr.fcfs_stdev,2), "   ", round(rndmgr.fcfs_variance, 2))
    print(" SSTF        ", round(rndmgr.sstf_mean, 2), "         ", round(rndmgr.sstf_stdev,2), "   ", round(rndmgr.sstf_variance, 2))
    print(" LOOK        ", round(rndmgr.look_mean, 2), "         ", round(rndmgr.look_stdev,2), "   ", round(rndmgr.look_variance, 2))
    print(" CLOOK       ", round(rndmgr.clook_mean, 2), "         ", round(rndmgr.clook_stdev,2), "   ", round(rndmgr.clook_variance, 2))
        