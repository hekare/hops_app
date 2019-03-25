var tasks = [];
for  (i = 0; i < valitut.length; i++) {
      tasks.push({"taskName":valitut[i][0], "startDate":new Date(valitut[i][1]),"endDate":new Date(valitut[i][2])});
}
tasks.sort(function(a, b) {
      return a.endDate - b.endDate;
});
var format = "%m.%Y";

var gantt = d3.gantt().taskTypes(names).tickFormat(format).height(names.length*50).width(1200);
gantt(tasks);
gantt.timeDomain([ d3.time.day.offset(getEndDate(), -7), getEndDate() ]);

function getEndDate() {
      var lastEndDate = Date.now();
      if (tasks.length > 0) {
            lastEndDate = tasks[tasks.length - 1].endDate;
      }
      return lastEndDate;
}