var tasks = [
      {"startDate":new Date("Sun Dec 09 01:36:45 EST 2012"),"endDate":new Date("Sun Dec 09 04:36:45 EST 2012"),"taskName":"VENA7","status":"SIVUAINE"}];

      var format = "%Y";
      var gantt = d3.gantt().taskTypes(taskNames).tickFormat(format).height(taskNames.length*50);      
      gantt(tasks);