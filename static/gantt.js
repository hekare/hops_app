var courseStatus = {
      "SUCCEEDED" : "bar-passed",
      "NOT_DONE" : "bar-not-passed",
      "RUNNING" : "bar-running",
  };
var tasks = [];
var today = new Date()
for  (i = 0; i < valitut.length; i++) {
      var start = new Date(valitut[i][1]);
      var end = new Date(valitut[i][2]);
      if(today > end){
            var status = "SUCCEEDED";
      }else if (today < start){
            var status = "NOT_DONE"
      }else{
            var status = "RUNNING"
      }
      tasks.push({"taskName":valitut[i][0], "startDate":start,"endDate":end, "status":status, "courseName":valitut[i][4], "nopat":valitut[i][5]});
}
tasks.sort(function(a, b) {
      return a.endDate - b.endDate;
});
var format = "%m.%Y";


var gantt = d3.gantt().taskTypes(names).taskStatus(courseStatus).tickFormat(format).height(names.length*50).width(1150);
gantt(tasks);
//gantt.timeDomainMode("fit")
gantt.timeDomain([ d3.time.day.offset(getEndDate(), -7), getEndDate() ]);

function getEndDate() {
      var lastEndDate = Date.now();
      if (tasks.length > 0) {
            lastEndDate = tasks[tasks.length - 1].endDate;
      }
      return lastEndDate;
}

d3.selectAll('.gantt-chart rect')
      .on('mouseover', function (obj) {hoverOver(this, obj)} )
      .on('mouseout', hoverOff)

function hoverOver (ctx, bar) {
      var dimBar = ctx.getBoundingClientRect()

      d3.select('#tooltip-name').text(bar.courseName)
      d3.select('#tooltip-nopat').text(bar.nopat)
      d3.select('#tooltip-start-day').text(bar.startDate.getDate())
      d3.select('#tooltip-start-month').text(bar.startDate.getMonth()+1)
      d3.select('#tooltip-start-year').text(bar.startDate.getFullYear())
      d3.select('#tooltip-end-day').text(bar.endDate.getDate())
      d3.select('#tooltip-end-month').text(bar.endDate.getMonth()+1)
      d3.select('#tooltip-end-year').text(bar.endDate.getFullYear())

      var dimTip = document.getElementById('tooltip')
      .getBoundingClientRect()     

      d3.select('#tooltip')
      .style('left', (dimBar.left + dimBar.width / 2 - dimTip.width / 2) + 'px')
      .style('top', (window.scrollY + dimBar.top - dimTip.height / 2 - 10) + 'px')
      .transition().duration(200)
      .style('opacity', 1)
      }
      
function hoverOff () {
      d3.select('#tooltip')
      .transition().duration(200)
      .style('opacity', 0)
}
