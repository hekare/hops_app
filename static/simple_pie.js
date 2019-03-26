
var canvasWidth = 450,
      canvasHeight = 400, 
      outerRadius = 150, 
      color = ["#377D22", "#808080", "#5a5a5a"];

var vis = d3.select("#pie")
      .append("svg:svg")
      .data([dataSet]) 
      .attr("width", canvasWidth)
      .attr("height", canvasHeight)
      .append("svg:g")
      .attr("transform", "translate(" + 1.5*outerRadius + "," + 1.5*outerRadius + ")")

var arc = d3.svg.arc().outerRadius(outerRadius);

var pie = d3.layout.pie()
      .value(function(d) { return d.magnitude; })
      .sort( function(d) { return null; } );

var arcs = vis.selectAll("g.slice")
      .data(pie)
      .enter()
      .append("svg:g")
      .attr("class", "slice");

arcs.append("svg:path")
      .attr("fill", function(d, i) { return color[i]; } )
      .attr("d", arc);

arcs.append("svg:text")
      .attr("transform", function(d) { 
            d.outerRadius = outerRadius + 50; 
            d.innerRadius = outerRadius + 45;
            return "translate(" + arc.centroid(d) + ")";
      })
      .attr("text-anchor", "middle")
      .style("fill", "Black")
      .style("font", "bold 15px Arial")
      .text(function(d, i) { return dataSet[i].legendLabel; });

arcs.filter(function(d) { return d.endAngle - d.startAngle > .2; }).append("svg:text")
      .attr("dy", ".35em")
      .attr("text-anchor", "middle")
      .attr("transform", function(d) { 
            d.outerRadius = outerRadius;
            d.innerRadius = outerRadius/2; 
            return "translate(" + arc.centroid(d) + ")";
      })
      .style("fill", "White")
      .style("font", "bold 20px Arial")
      .text(function(d) { return d.data.magnitude; });