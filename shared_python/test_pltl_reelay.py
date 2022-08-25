import reelay

#order = l1,l2,l3

class CMonitorWrapper(object):
    def __init__(self,name,prop,mon_obj):
        self._name = name
        self._prop = prop
        self._mon_obj = mon_obj
        self.tracelist = None
        self._final_trace_and_verdict = None

    def generate_monitor(self):
        pattern = self._prop
        self._mon_obj=reelay.discrete_timed_monitor(pattern=pattern,condense=False)

    def __repr__(self):
        return "{0}: {1}".format(self._name,self._prop)

    def update(self,x):
        return self._mon_obj.update(x)
    
    def monitor(self):
        return self._mon_obj

    def add_tracename(self,tracename):
        if self.tracelist is None:
            self.tracelist = {}
        if tracename not in self.tracelist:
            self.tracelist[tracename] = []
            
    def add_trace(self,tracename,aps,trace,value):
        self.add_tracename(tracename)
        trace_dict = {"propvalues": aps, "tracesofar":trace, "verdict":value}
        self.tracelist[tracename].append(trace_dict)

    def get_trace_changes(self,tracename):
        changes = []
        if self.tracelist is not None:
            if tracename in self.tracelist:
                traces = self.tracelist[tracename]
                initial_verdict = traces[0]["verdict"]
                changes.append(traces[0])
                for i in range(1,len(traces)):
                    if traces[i]["verdict"] != initial_verdict:
                        changes.append(traces[i])
                        initial_verdict=traces[i]["verdict"]
        return changes

    def final_verdict(self,tracename):
        if self._final_trace_and_verdict is None:
            self._final_trace_and_verdict = {}
        if tracename not in self._final_trace_and_verdict:
            self._final_trace_and_verdict[tracename] = None
        if self._final_trace_and_verdict[tracename] is None:
            self._final_trace_and_verdict[tracename] = self.tracelist[tracename][-1]

        return self._final_trace_and_verdict[tracename]

    def print_trace(self,tracename):
        if self.tracelist is not None:
            if tracename in self.tracelist:
                traces = self.tracelist[tracename]
                for i in range(len(traces)):
                    print("{0}-{1}: {2}".format(traces[i]["propvalues"],traces[i]["tracesofar"],traces[i]["verdict"]))

                        
        


DEFAULT_VISIT_STRING = r"(once{l1:true} and once{l2:true} and once{l3:true})"
START_AP = "start"

def all_false(aps):
    trace_dict = {}
    for ap in aps:
        trace_dict[ap]=False
    return trace_dict

def generate_trace(aps,trace):
    trace_list = []
    trace_dict = all_false(aps)
    if START_AP in aps:
        trace_dict[START_AP]=True
    trace_list.append(trace_dict)

    for ap in trace:
        trace_dict = all_false(aps)
        trace_dict[ap] = True
        trace_list.append(trace_dict)

    trace_dict = all_false(aps)
    trace_list.append(trace_dict)
    
    return trace_list

def get_test_traces():
    aps=["l1","l2","l3","l4",START_AP]
    tracelist_human = {}
    tracelist_dict = {}

    #test traces
    test_traces=["l1",
                 "l2,l1"]

    for i in range(len(test_traces)):
        trace=test_traces[i]
        test_trace = trace.split(',')
        test_tracelist = generate_trace(aps,test_trace)
        trace_label = "test_trace{0}".format(i)
        tracelist_dict[trace_label]=test_tracelist
        tracelist_human[trace_label]=trace

    return (tracelist_dict,tracelist_human)


def generate_monitor(pattern):
    return reelay.discrete_timed_monitor(pattern=pattern,condense=False)


def add_monitor(name, prop_str, mon, monitors):
    
    monitors[name] = CMonitorWrapper(name,prop_str,mon)
    return monitors

def combine_clauses(clause_list):
    combined_clause = r"("
    combined_clause+= " and ".join(clause_list)
    combined_clause+=r")"
    #print (combined_clause)
    return combined_clause
        


def add_test_mon1(monitors):
    #ordered visit
    prop_name = "test_prev_trace"
    visit_string =r" (once ({start:true}) -> ( once ({l1:true} and (pre{start:true})) ))"
    ordered_visit_string =combine_clauses([visit_string])
    ordered_visit_mon = generate_monitor(ordered_visit_string)
    monitors=add_monitor(prop_name, ordered_visit_string, ordered_visit_mon, monitors)
    return monitors

def add_test_mon2(monitors):
    #ordered visit
    prop_name = "test_prev_trace2"
    visit_string =r" (once ({start:true}) -> (  ({l1:true} since (pre{start:true})) ))"
    ordered_visit_string =combine_clauses([visit_string])
    ordered_visit_mon = generate_monitor(ordered_visit_string)
    monitors=add_monitor(prop_name, ordered_visit_string, ordered_visit_mon, monitors)
    return monitors


def generate_monitors():
    monitors = {}

    monitors = add_test_mon1(monitors)
    monitors = add_test_mon2(monitors)


    return monitors




def check_traces_using_monitors():
    #(traces,traces_strs) = get_example_traces_dict()
    (traces,traces_strs)=get_test_traces()
    mons = generate_monitors()

    for mon in mons:
        for trace in traces:
            #for each trace add the trace to the monitor
            mons[mon].add_tracename(traces_strs[trace])

    #for each trace go through the monitors
    for trace in traces:
        tracelist = traces[trace]
        trace_so_far=''
        for mon in mons:
            mons[mon].generate_monitor()
            
        for trace_elem in tracelist:
            traces_true_here = '('
            for k in trace_elem:
                if trace_elem[k] == True:
                    traces_true_here +=k+','
            traces_true_here+=')'
            if traces_true_here != '()':
                trace_so_far += traces_true_here +", "
            
            for mon in mons:
                rmon = mons[mon].update(trace_elem)
                mons[mon].add_trace(traces_strs[trace],trace_elem,str(trace_so_far),rmon["value"])



    print("All traces")
    for mon in mons:
        print("Monitor {0}".format(mon))
        for trace in traces:
            print("Trace {0}: {1}".format(trace,traces_strs[trace]))
            mons[mon].print_trace(traces_strs[trace])
            
            
    print("Sequences where verdicts changed values")
    for mon in mons:
        print("Monitor {0}".format(mon))
        for trace in traces:
            print("Trace {0}: {1}".format(trace,traces_strs[trace]))
            for part_trace in mons[mon].get_trace_changes(traces_strs[trace]):
                tracesofar = part_trace["tracesofar"]
                print("{0} : {1}".format(tracesofar,part_trace["verdict"]))

    #final verdicts
    print("Final Verdicts")
    for mon in mons:
        import pprint
        pp=pprint.PrettyPrinter()
        pp.pprint("Property {0}".format(mons[mon]._prop))
        for trace in traces:
            final_verdict = mons[mon].final_verdict(traces_strs[trace])
            tracesofar=','.join(k for k in final_verdict['tracesofar'])
            final_value = final_verdict['verdict']
            print("{0}: {1} ({2}) {3}".format(mon,trace,traces_strs[trace],final_value))


    
                      
            
                
if __name__ == "__main__":
    check_traces_using_monitors()
