function render_chart(data){
var margin = {top: 40, right: 20, bottom: 30, left: 120},
    width = 960 - margin.left - margin.right,
    height = 400 - margin.top - margin.bottom;

var parseDate = d3.time.format("%Y-%m-%d-%H-%M-%S").parse;

var x = d3.time.scale()
    .range([0, width]);

var y = d3.scale.linear()
    .range([height, 0]);

var xAxis = d3.svg.axis()
    .scale(x)
    .orient("bottom");

var yAxis = d3.svg.axis()
    .ticks(5)
    .scale(y)
    .tickFormat(function (d) {
      for (key in levels){
        if (levels[key]['value'] == d){return levels[key]['display'];}
      }
      return '';
    })
    .orient("left");

var line = d3.svg.line()
    .x(function(d) { return x(d.date); })
    .y(function(d) { return y(d.level_value); });


var levels = {
  'out': {'value':0,'display':'Out of Coffee'},
  'low': {'value':1,'display':'Not Much Left'},
  'medium': {'value':2,'display':"Some"},
  'high': {'value':3,'display':"Plenty"},
  'full':{'value':4,'display':"Tons of Coffee"}
}

data.forEach(function(d) {
    console.log(d.value);
  });


  data.forEach(function(d) {
    d.date = parseDate(d.year+'-'+d.month+'-'+d.day+'-'+d.hour+'-'+d.minute+'-'+0);
    console.log(d.date);
    d.level_value = +levels[d.level]['value'];
    d.value = +d.value;
    console.log(d);
  });

  var svg = d3.select("#chart").append("svg")
      .attr("width", width + margin.left + margin.right)
      .attr("height", height + margin.top + margin.bottom)
      .attr("class","line-chart")
    .append("g")
      .attr("transform", "translate(" + margin.left + "," + margin.top + ")");


    x.domain(d3.extent(data, function(d) { return d.date; }));
    y.domain([0, d3.max(data, function(d) { return d.level_value; })]);

    svg.append("path")
        .datum(data)
        .attr("class", "line")
        .attr("d", line);

    svg.append("g")
        .attr("class", "x axis")
        .attr("transform", "translate(0," + height + ")")
        .call(xAxis);

    svg.append("g")
        .attr("class", "y axis")
        .call(yAxis)
      .append("text")
        .attr("transform", "rotate(-90)")
        .attr("y", 6)
        .attr("dy", ".71em")
        .style("text-anchor", "end")
        .text("Coffee Level");
}

function update_data(timeDifference){
  data = logs;
  var today = new Date();
  var new_data = [];
  console.log("Difference: " + timeDifference);
  for (var item in data){
    if(((today - data[item].date)/1000/60/60/24) < timeDifference){
      new_data.push(data[item]);
    }
  }
  return new_data;
}

// var data = logs;
render_chart(logs);

$('#week').on('click', function () {
  d3.selectAll(".line-chart").remove();
  var new_data = update_data(7);
  render_chart(new_data);
});

$('#month').on('click', function () {
  d3.selectAll(".line-chart").remove();
  var new_data = update_data(30);
  render_chart(new_data);
});

$('#year').on('click', function () {
  d3.selectAll(".line-chart").remove();
  var new_data = update_data(365);
  render_chart(new_data);
});
