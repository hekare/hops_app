!function(){
      var gradPie={};

      var pie = d3.layout.pie().sort(null).value(function(d) {return d.value;});

      createGradients = function(defs, colors, r){	
            var gradient = defs.selectAll('.gradient')
                  .data(colors).enter().append("radialGradient")
                  .attr("id", function(d,i){return "gradient" + i;})
                  .attr("gradientUnits", "userSpaceOnUse")
                  .attr("cx", "0").attr("cy", "0").attr("r", r).attr("spreadMethod", "pad");
                  
            gradient.append("stop").attr("offset", "0%").attr("stop-color", function(d){ return d;});

            gradient.append("stop").attr("offset", "30%")
                  .attr("stop-color",function(d){ return d;})
                  .attr("stop-opacity", 1);
                  
            gradient.append("stop").attr("offset", "70%")
                  .attr("stop-color",function(d){ return "black";})
                  .attr("stop-opacity", 1);
      }

      gradPie.draw = function(id, data, cx, cy, r){
            var gPie = d3.select("#"+id).append("g")
                  .attr("transform", "translate(" + cx + "," + cy + ")");
                  
            createGradients(gPie.append("defs"), data.map(function(d){ return d.color; }), 100*r);

            gPie.selectAll("path").data(pie(data))
                  .enter().append("path").attr("fill", function(d,i){ return "url(#gradient"+ i+")";})
                  .attr("d", d3.svg.arc().outerRadius(r))
                  .each(function(d) { this._current = d; });
	
      }

      gradPie.transition = function(id, data, r) {
            function arcTween(a) {
                  var i = d3.interpolate(this._current, a);
                  this._current = i(0);
                  return function(t) { return d3.svg.arc().outerRadius(r)(i(t));  };
            }
            
            d3.select("#"+id).selectAll("path").data(pie(data))
                  .transition().duration(750).attrTween("d", arcTween); 
      }	

      this.gradPie = gradPie;
}();

var salesData=[
      {label:"nopat", value: 100, color:"#377D22"},
      {label:"puuttuu kandista", value: 80, color:"#808080"},
      {label:"puuttuu dipasta", value: 120, color:"#5a5a5a"},
];
var svg = d3.select("#pie").append("svg").attr("width", 700).attr("height", 400);
svg.append("g").attr("id","salespie");
gradPie.draw("salespie", salesData, 200, 200, 160);