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

def get_example_traces_dict():
    aps=["l1","l2","l3","l4",START_AP]
    tracelist_human = {}
    tracelist_dict = {}


    #incomplete trace
    incomplete_trace = ["l3","l4","l1"]
    incomplete_tracelist = generate_trace(aps,incomplete_trace)
    tracelist_dict["incomplete"]=incomplete_tracelist
    tracelist_human["incomplete"]=' '.join(incomplete_trace)
    
    #out of order trace
    outoforder_trace = ["l2","l1","l4","l3","l2"]
    outoforder_tracelist = generate_trace(aps,outoforder_trace)
    tracelist_dict["outoforder"]=outoforder_tracelist
    tracelist_human["outoforder"] = '  '.join(outoforder_trace)

    #seq_visit
    sequenced_trace = ["l1","l3","l1","l2","l4","l3","l2"]
    sequenced_tracelist = generate_trace(aps,sequenced_trace)
    tracelist_dict["sequenced"] = sequenced_tracelist
    tracelist_human["sequenced"] = '  '.join(sequenced_trace)

    #ordered_visit
    ordered_trace = ["l1","l4","l1","l2","l4","l3","l1"]
    ordered_tracelist = generate_trace(aps,ordered_trace)
    tracelist_dict["ordered"] = ordered_tracelist
    tracelist_human["ordered"] = '  '.join(ordered_trace)

    #strict_ordered_visit
    strict_ordered_trace = ["l1","l4","l2","l4","l3","l1"]
    strict_ordered_tracelist = generate_trace(aps,strict_ordered_trace)
    tracelist_dict["strict_ordered"] = strict_ordered_tracelist
    tracelist_human["strict_ordered"] = '  '.join(strict_ordered_trace)

    #fair_visit
    fair_trace = ["l1","l4","l3","l1","l4","l2","l2","l4"]
    fair_tracelist = generate_trace(aps,fair_trace)
    tracelist_dict["fair_visit"] = fair_tracelist
    tracelist_human["fair_visit"] = '  '.join(fair_trace)

    #fair_strict_ordered_visit
    fair_strict_ordered_trace = ["l1","l4","l2","l4","l3","l1","l2","l3"]
    fair_strict_ordered_tracelist = generate_trace(aps,fair_strict_ordered_trace)
    tracelist_dict["fair_strict_ordered"] = fair_strict_ordered_tracelist
    tracelist_human["fair_strict_ordered"] = '  '.join(fair_strict_ordered_trace)


   
    return (tracelist_dict,tracelist_human)


def get_test_traces():
    aps=["l1","l2","l3","l4",START_AP]
    tracelist_human = {}
    tracelist_dict = {}

    #test traces
    test_traces=["l1,l1,l1",
                 "l4,l4,l4",
                 "l4,l4,l1",
                 "l1,l2,l3",
                 "l1,l4,l1,l2,l4,l3",
                 "l4,l1,l4,l2,l4,l3,l4,l1",
                 "l3,l2,l1",
                 "l1,l3,l2,l3",
                 "l1,l2,l1,l2,l3,l2,l1",
                 "l1,l4,l1,l3,l1,l4,l2,l4",
                 "l4,l1,l4,l2,l4,l3",
                 "l1,l2,l3,l1,l2,l3",
                 "l3,l1,l2,l3,l1,l2",
                 "l4,l3,l1,l2,l3",
                 "l4,l3,l1,l2,l3,l1",
                 "l1,l3,l1,l2,l3"]

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
        


def add_visit_monitor(monitors):
    #simple visit monitor
    visit_string = r"(once{l1:true} and once{l2:true} and once{l3:true})"
    
    visit_monitor = generate_monitor(visit_string)
    monitors = add_monitor("visit",visit_string,visit_monitor,monitors)

    #end simple visit monitor
    return monitors

def add_sequenced_visit_monitor(monitors):
    # sequential visit monitor
    seq_visit_string=r"(( once ( {l3:true} and ( once ( {l2:true} and (once{l1:true})  )  )  ) ))"
    seq_visit_mon = generate_monitor(seq_visit_string)
    monitors = add_monitor("seq_visit",seq_visit_string,seq_visit_mon,monitors)
    #end sequential visit monitor

    return monitors

def add_ordered_visit_monitor(monitors):
    #ordered visit
    prop_name = "ordered_visit"
    visit_string = r"(once{l1:true} and once{l2:true} and once{l3:true})"
    l1_true_l2_false_before=r"(once({l1:true} and (historically{l2:false})))"
    l2_true_l3_false_before=r"(once({l2:true} and (historically{l3:false})))"
    ordered_visit_string =combine_clauses([l1_true_l2_false_before,l2_true_l3_false_before,visit_string])
    ordered_visit_mon = generate_monitor(ordered_visit_string)
    monitors=add_monitor(prop_name,ordered_visit_string,ordered_visit_mon,monitors)


    return monitors



def add_superstrict_monitor(monitors):
    visit_string = DEFAULT_VISIT_STRING
    # strict ordered monitor?
    l1_visit = r"(historically({l1:true} -> (historically{l2:false,l3:false})))"
    l2_visit = r"(historically({l2:true} -> (historically{l3:false})))"

    ordered_visit_historically_string = r"("+visit_string+" and "+l1_visit+" and "+l2_visit+")"
    ordered_visit_monitor_historically = generate_monitor(ordered_visit_historically_string)

    monitors=add_monitor("superstrict_ordered_visit",ordered_visit_historically_string,ordered_visit_monitor_historically,monitors)
    return monitors

def add_ordered_visit_monitor2(monitors):

    visit_string = DEFAULT_VISIT_STRING

    l1_visit_alt = r"(once({l1:true} and (historically{l2:false,l3:false})))"
    l2_visit_alt = r"(once({l2:true} and (historically{l3:false})))"
    l3_visit = r"(once{l3:true})"


    ordered_visit_once_string =combine_clauses([l1_visit_alt,
                                                l2_visit_alt,
                                                l3_visit])

    ordered_visit_monitor_once = generate_monitor(ordered_visit_once_string)
    monitors=add_monitor("ordered_visit_var",ordered_visit_once_string,ordered_visit_monitor_once,monitors)

    #end strict ordered monitor
    return monitors


def add_strict_ordered_visit_monitor(monitors):
    #ordered visit
    prop_name = "strict_ordered_visit"
    visit_string =r" (once(({l3:false} since ({l3:true} and (pre(historically{l3:false})) )) and  (({l2:false} since ({l2:true} and (pre(historically{l2:false}))) ) and ( {l1:false} since ( {l1:true} and (pre(historically{l1:false}))  )  ) ))) "#r" (once({l2:true} and ( once({l1:true} and (pre(historically{l1:false}))))))   "
    seq_visit_string=r"(( once ( {l3:true} and ( once ( {l2:true} and (once{l1:true})  )  )  ) ))"
    ordered_visit_string =combine_clauses([visit_string,seq_visit_string])
    ordered_visit_mon = generate_monitor(ordered_visit_string)
    monitors=add_monitor(prop_name, ordered_visit_string, ordered_visit_mon, monitors)
    return monitors


def add_strict_ordered_visit_monitor_nested(monitors):
    #ordered visit
    prop_name = "strict_ordered_visit_nested"
    visit_string =r" (once( {l3:false} since ( {l3:true} and ( pre( historically{l3:false} and ( {l2:false} since ( {l2:true} and ( pre ( historically{l2:false} and ( {l1:false} since ( {l1:true} and (pre(historically{l1:false}))  )  )  )  )  )  ))  )  )))   "
    seq_visit_string=r"(( once ( {l3:true} and ( once ( {l2:true} and (once{l1:true})  )  )  ) ))"
    ordered_visit_string =combine_clauses([visit_string,seq_visit_string])
    ordered_visit_mon = generate_monitor(ordered_visit_string)
    monitors=add_monitor(prop_name, ordered_visit_string, ordered_visit_mon, monitors)
    return monitors

def add_strict_ordered_visit_monitor_m(monitors):
    prop_name = "temp_super_strict_ordered_visit"
    l1_prop =r"({l1:false} since ({l1:true} and (({l1:false,l2:false,l3:false}) since {start:true})))"
    #l2_prop = "({l2:false} since ({l2:false}))"
    l2_prop =r"({l2:false} since ({l2:true} and (({l2:false,l3:false}) since {start:true})))"
    l3_prop=r"({l3:false} since ({l3:true} and ({l3:false} since {start:true})))"
    full_prop = combine_clauses([l1_prop,l2_prop,l3_prop])
    monitor = generate_monitor(full_prop)
    monitors=add_monitor(prop_name,full_prop,monitor,monitors)
    return monitors


def add_fair_visit_monitor_test(monitors):
    prop_name = "fair_visit"
    l1_prop=r"(historically({l1:true} -> (pre(historically({l1:false} or (once({l3:true})))))))"
    l1_prop_1=r"(historically({l1:true} -> (pre((once{l3:true}) since (once{l1:true})))))"
    l1_prop_2=r"(historically({l1:true} -> (pre(historically{l1:false}))))"
    l1_prop = "("+l1_prop_1 + " or "+l1_prop_2+")"
    #l1_prop ="(historically({l1:true} -> (pre((historically{l1:false}) or ((once{l3:true}) since ({l1:true}))))))"
    l2_prop=r"(historically({l2:true} -> (pre((historically{l2:false}) or ((once{l1:true}) since (once{l2:true}))))))"
    l3_prop=r"(historically({l3:true} -> (pre((historically{l3:false}) or ((once{l2:true}) since (once{l3:true}))))))"
    visit_prop = DEFAULT_VISIT_STRING
    full_prop = combine_clauses([l1_prop,
                                 l2_prop,l3_prop,
                                 visit_prop
                                 ])
    monitor = generate_monitor(full_prop)
    monitors = add_monitor(prop_name,full_prop,monitor,monitors)
    return monitors

def add_fair_visit_monitor(monitors):
    prop_name = "fair_visit"
    l1_prop=r"(historically({l1:true} -> (pre(historically({l1:false} or (once({l3:true})))))))"
    l1_prop_1=r"(historically({l1:true} -> (pre((once{l3:true})))))"
    l1_prop_2=r"(historically({l1:true} -> (pre(historically{l1:false}))))"
    l1_prop = "("+l1_prop_1 + " or "+l1_prop_2+")"
    l1_prop ="(historically({l1:true} -> (pre((historically{l1:false}) or ((once{l3:true}) since ({l1:true}))))))"
    l2_prop=r"(historically({l2:true} -> (pre((historically{l2:false}) or ((once{l1:true}) since ({l2:true}))))))"
    l3_prop=r"(historically({l3:true} -> (pre((historically{l3:false}) or ((once{l2:true}) since ({l3:true}))))))"
    visit_prop = DEFAULT_VISIT_STRING
    full_prop = combine_clauses([l1_prop,
                                 l2_prop,l3_prop,
                                 visit_prop])
    monitor = generate_monitor(full_prop)
    monitors = add_monitor(prop_name,full_prop,monitor,monitors)
    return monitors


def generate_monitors():
    monitors = {}

    #monitors=add_visit_monitor(monitors)
    #monitors=add_sequenced_visit_monitor(monitors)
    monitors=add_ordered_visit_monitor(monitors)
    #monitors=add_strict_ordered_visit_monitor(monitors)
    monitors = add_ordered_visit_monitor2(monitors)
    #monitors = add_superstrict_monitor(monitors)
    monitors = add_strict_ordered_visit_monitor(monitors)
    monitors = add_strict_ordered_visit_monitor_nested(monitors)
    #monitors = add_strict_ordered_visit_monitor_m(monitors)

    #monitors = add_fair_visit_monitor_test(monitors)

    return monitors




def check_traces_using_monitors():
    (traces,traces_strs) = get_example_traces_dict()
    #(traces,traces_strs)=get_test_traces()
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
