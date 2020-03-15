import pandas as pd 
import ast
import random
data=pd.read_csv("Large_scale_dataset.csv")
output_twt=[]
output_tt=[]
output_n=[]
output_twte=[]
output_tte=[]
output_ne=[]
output_pt=[]
output_s=[]
output_p=[]
output_dd=[]
output_rt=[]
output_greedy=[]
output_greedyt=[]
output_greedyn=[]
output_greedye=[]
output_greedyte=[]
output_greedyne=[]





n_iterations=10
mi_over_iterations=-190
mi_t_over_iterations=0
mi_n_over_iterations=0
i_for_data=0
for ijkl in range(n_iterations*640):
    #pt -processing time | s-size | rt-release time | dd-due date
    pt=ast.literal_eval(data['Processing time'].iloc[i_for_data])
    s=ast.literal_eval(data['Size'].iloc[i_for_data])
    rt=ast.literal_eval(data['Release time'].iloc[i_for_data])
    dd=ast.literal_eval(data['Due-date'].iloc[i_for_data])
    
    # print(pt)
    # print(s)
    # print(rt)
    # print(dd)
    
    size=len(pt)
    #print(ijkl+1)
    batch_capacity=20

    # initialise weights to 1
    w=[1 for _ in range(size)]

    ep=100
    

    wtotal=0 #completion time of induvidual batch
    twt=0
    e=0
    alpha=8/500000
    lower_bound=0
    global_minimum=1000000
    global_minimum_n=0
    global_minimum_t=0
    global_minimum_ne=0
    global_minimum_te=0
    global_minimume=0
    prev_twt=-100
    if(size==50):
        alpha=8/5000000
    elif(size==75):
        alpha=8/50000000
    elif(size==100):
        alpha=8/500000000



    for epochs in range(ep):
        sb=[0 for _ in range(size)] #size of the batch
        b=[[] for _ in range(size)] #batch index
        #calculated difference between previous TWT and lower bound which is taken as 0

        e=twt
        twt=0
        wtotal=0
        prev_w=[]
        n_repeats=0 #count of number of times same solution occurs
        # storing a copy of the present weights before updating
        for i in range(size):
            prev_w.append(w[i])

        # weight updation using learning strategy 
        if(epochs!=0):
            for lcv in range(size):
                ran=random.uniform(0,1)
                if(ran>0.5):
                    w[lcv]=w[lcv]-alpha*e*ran
                else:
                    w[lcv]=w[lcv]+alpha*e*ran
            #reinforcement with reinforcement factor set to 4
            for lcv in range(size):
                w[lcv]=w[lcv]+4*(w[lcv]-prev_w[lcv])




        #print(w)
        #print(p)

        # pw- objective function . Job with maximum pw is selected first.
        ciratio=(dd[i]-pt[i])
        pw=[w[i]*s[i] for i in range(size)]
        
        
        batch=0
        # b- stores the batches as a list
        b=[[]]
        m=0
        j=0
        jobs=0

        #alloting jobs to batches
        while jobs<size:
            
            m=-1000000000000
            j=0

            #Loop to identify job with highest characteristic function(pw)
            for i in range(size):
                if(pw[i]>m):
                    m=pw[i]
                    j=i
            # if(epochs==ep-1):
            #     print(pw[j])
            

            pw[j]=-10000000000  # this is to mark that job as done
            batch=0
            while (sb[batch]+s[j]>batch_capacity):
                
                
                batch=batch+1

                b.append([])
            
            #updating size of the present batch
            sb[batch]=sb[batch]+s[j]
            # total_time=0
            # nl=[]
            b[batch].append(j+1)
        
            jobs=jobs+1

        total_time=0
        n1=[]
        
        n1=[]
        for r in b:
                ma=0
                for rd in r:
                    
                    if(pt[rd-1]>ma):
                        ma=pt[rd-1]
                    
                total_time=total_time+ma
                if(len(r)==0):
                    break
                bv=ma/len(r)
                #nl.append(bv)

        
        #printing
        twt=0
        tt=0
        tnum=0
        tet=0
        tenum=0
        tte=0

        #the following lines are for calculating the total weighted tardiness for the batches formed
        if(epochs>=0):
           
            ij=0
           # print("Epoch ")
            # print(epochs+1)
            va=0
            
            while va<len(b):
                mi=1000000
                
                
                # if(epochs==0):
                #     print(b[va])
                
                
                max_pro=0
                # loop to find maximum processing time of all jobs in this batch
                for sj in b[va]:
                    if(pt[sj-1]>max_pro):
                        max_pro=pt[sj-1]
                max_rel=0
                for sj in b[va]:
                    if(rt[sj-1]>max_rel):
                        max_rel=rt[sj-1]

                max_rel1=max(max_rel,wtotal)
                #print(max_rel1," ",max_rel)
                for sj in b[va]:
                    if((max_pro+max_rel1-dd[sj-1])>0):
                        tnum=tnum+1
                        #print(dd[sj-1])
                        #print(s[sj-1],wtotal+max_pro+max_rel,dd[sj-1])
                        twt=twt+s[sj-1]*(max_pro+max_rel1-dd[sj-1])
                        tt=tt+(max_pro+max_rel1-dd[sj-1])
                    else:
                        tet=tet+s[sj-1]*(max_pro+max_rel1-dd[sj-1])*-1
                        tenum=tenum+1
                        tte=tte+(max_pro+max_rel1-dd[sj-1])*-1
                wtotal=max_pro+max_rel1
                #print(wtotal)
                #print(b[va])

                #print("twt for each batch",twt)




                #nl[va]=100000000
                ij=ij+1
                va=va+1
        

        if(prev_twt==-100 and ijkl%n_iterations==0):
            output_greedy.append(twt)
            output_greedyt.append(tt)
            output_greedyn.append(tnum)
            output_greedye.append(tet)
            output_greedyte.append(tte)
            output_greedyne.append(tenum)
            #print(twt)

        # if the solution is worse than previous solution then update back to previous weights. 
        if(prev_twt!=-100):# if it is not first epoch
            if(twt>prev_twt):
                for i in range(size):
                    w[i]=prev_w[i]
                ep=ep+1
            elif(twt==prev_twt):
                n_repeats=n_repeats+1
                
            else:
                prev_twt=twt
                n_repeats=0
        else:
            prev_twt=twt

        if(n_repeats==10):
            break
        
        if(twt<global_minimum):
            global_minimum=twt
            global_minimum_t=tt
            global_minimum_n=tnum
            global_minimume=tet
            global_minimum_te=tte
            global_minimum_ne=tenum

        # print("total weighted tardiness = ",twt)
        # print("total tardiness =",tt)
        # print("number of tardy jobs",tnum)
    # print("twt",global_minimum)
    # print("total tardiness",global_minimum_t)
    # print("number of tardy jobs",tnum)

    if(ijkl%n_iterations==0):
        mi_over_iterations=global_minimum
        mi_n_over_iterations=global_minimum_n
        mi_t_over_iterations=global_minimum_t
        mi_over_iterationse=global_minimume
        mi_n_over_iterationse=global_minimum_ne
        mi_t_over_iterationse=global_minimum_te
        #print("first")
    elif(ijkl%n_iterations!=0):
        # print(global_minimum,global_minimum_t,global_minimum_n)
        if(global_minimum<mi_over_iterations):
            mi_over_iterations=global_minimum
            mi_t_over_iterations=global_minimum_t
            mi_n_over_iterations=global_minimum_n
            mi_over_iterationse=global_minimume
            mi_n_over_iterationse=global_minimum_ne
            mi_t_over_iterationse=global_minimum_te
        #print("Minimum now is",mi_over_iterations)
    if(ijkl%n_iterations==n_iterations-1):
        #print("total weighted tardiness = ",mi_over_iterations)
        output_twt.append(mi_over_iterations)
        output_tt.append(mi_t_over_iterations)
        output_n.append(mi_n_over_iterations)
        output_twte.append(mi_over_iterationse)
        output_tte.append(mi_t_over_iterationse)
        output_ne.append(mi_n_over_iterationse)
        # print(mi_over_iterations,mi_t_over_iterations,mi_n_over_iterations)
        print(i_for_data+1)
        i_for_data=i_for_data+1
        



    
    # print("number of tardy jobs= ",global_minimum_n)
    
    
    #print(pt)
    
    
    
    
    
    # output_twt.append(global_minimum)
    # output_tt.append(global_minimum_t)
    # output_n.append(global_minimum_n)
    # output_pt.append(pt)
    # output_s.append(s)
    
    # output_rt.append(rt)
    # output_dd.append(dd)

    # if(ijkl<=5):
    #     print(global_minimum)




    



import csv
from itertools import zip_longest

d = [output_twt,output_greedy,output_tt,output_greedyt,output_n,output_greedyn,output_twte,output_greedye,output_ne,output_greedyne,output_tte,output_greedyte]
export_data = zip_longest(*d, fillvalue = '')
with open('output_for_priority_onlytwt.csv', 'w', encoding="ISO-8859-1", newline='') as myfile:
      wr = csv.writer(myfile)
      wr.writerow(("TWT", "greedy twt","TT","greedy TT","tardy jobs","greed tardy jobs","Total weighted earliness","Total weighted earliness greedy","number of early jobs","number of early jobs greedy","total earliness","total earliness greedy"))
      wr.writerows(export_data)
myfile.close()