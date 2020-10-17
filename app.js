
// // set the dimensions and margins of the graph
var margin = {top: 20, right: 30, bottom: 30, left: 40},
    width = 460 - margin.left - margin.right,
    height = 400 - margin.top - margin.bottom;

// // append the svg object to the body of the page
// var svg = d3.select("#my_dataviz")
//   .append("svg")
//     .attr("width", 100000 || width + margin.left + margin.right)
//     .attr("height", 100000 ||height + margin.top + margin.bottom)
//   .append("g");
    // .attr("transform",
    //       "translate(" + margin.left + "," + margin.top + ")");

// // read data
// d3.csv("https://raw.githubusercontent.com/holtzy/D3-graph-gallery/master/DATA/data_for_density2d.csv", function(data) {

//   // Add X axis
//   var x = d3.scaleLinear()
//     .domain([5, 20])
//     .range([ 0, width ]);
//   svg.append("g")
//     .attr("transform", "translate(0," + height + ")")
//     .call(d3.axisBottom(x));

//   // Add Y axis
//   var y = d3.scaleLinear()
//     .domain([5, 22])
//     .range([ height, 0 ]);
//   svg.append("g")
//     .call(d3.axisLeft(y));

//   // compute the density data
//   var densityData = d3.contourDensity()
//     .x(function(d) { return x(d.x); })   // x and y = column name in .csv input data
//     .y(function(d) { return y(d.y); })
//     .size([width, height])
//     .bandwidth(20)    // smaller = more precision in lines = more lines
//     (data)

//   // Add the contour: several "path"
//   svg
//     .selectAll("path")
//     .data(densityData)
//     .enter()
//     .append("path")
//       .attr("d", d3.geoPath())
//       .attr("fill", "none")
//       .attr("stroke", "#69b3a2")
//       .attr("stroke-linejoin", "round")
// });









d3.csv("firms.csv",function(error,data) {dataViz(data)});

function dataViz(incData) {

  var nodeHash = {};
  var nodes = [];
  var edges = [];

  incData.forEach(function (edge) {
    if (!nodeHash[edge.source]) {
      nodeHash[edge.source] = {id: edge.source, label: edge.source};
      nodes.push(nodeHash[edge.source]);
    }
    if (!nodeHash[edge.target]) {
      nodeHash[edge.target] = {id: edge.target, label: edge.target};
      nodes.push(nodeHash[edge.target]);
    }
    if (edge.weight >= 5) {
      edges.push({source: nodeHash[edge.source], target: nodeHash[edge.target], weight: edge.weight});
    }
  });

  var force = d3.layout.force().nodes(nodes).links(edges)
  .size([500,500])
  .charge(-200)
  .on("tick", updateNetwork);

  d3.select("svg").selectAll("line")
  .data(edges)
  .enter()
  .append("line")
  .style("stroke-width", "1px")
  .style("stroke", "#CC9999");

  d3.select("svg").selectAll("circle")
  .data(nodes)
  .enter()
  .append("circle")
  .style("fill", "#996666")
  .attr("r", 5);

  force.start();

  function updateNetwork() {
    d3.select("svg").selectAll("line")
      .attr("x1", function (d) {return d.source.x})
      .attr("x2", function (d) {return d.target.x})
      .attr("y1", function (d) {return d.source.y})
      .attr("y2", function (d) {return d.target.y});

    d3.select("svg").selectAll("circle")
      .attr("cx", function (d) {return d.x})
      .attr("cy", function (d) {return d.y});
  }
}