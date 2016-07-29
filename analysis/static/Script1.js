var w = 500,
	h = 480;

var colorscale = d3.scale.category10();

//Legend titles
var LegendOptions = ['2015','2016'];

//Data
var d = [
		  [
			{axis:"Dissolved Oxygen",value:0.42},
			{axis:"Turbidity",value:0.05},
			{axis:"Water Temperature",value:0.07},
			{axis:"Salinity",value:0.07},
			{axis:"PH",value:0.18},
			{axis:"Chlorophyll",value:0.08}
		  ],[

			{axis:"Dissolved Oxygen",value:0.27},
			{axis:"Turbidity",value:0.05},
			{axis:"Water Temperature",value:0.08},
			{axis:"Salinity",value:0.06},
			{axis:"PH",value:0.19},
			{axis:"Chlorophyll",value:0.17}
		  ]
		];

//Options for the Radar chart, other than default
var mycfg = {
  w: w,
  h: h,
  maxValue: 0.6,
  levels: 6,
  ExtraWidthX: 300
}

//Call function to draw the Radar chart
//Will expect that data is in %'s
RadarChart.draw("#chart", d, mycfg);

////////////////////////////////////////////
/////////// Initiate legend ////////////////
////////////////////////////////////////////

var svg = d3.select('#body')
	.selectAll('svg')
	.append('svg')
	.attr("width", w+300)
	.attr("height", h)

//Create the title for the legend
var text = svg.append("text")
	.attr("class", "title")
	.attr('transform', 'translate(90,0)') 
	.attr("x", w - 80)
	.attr("y", 10)
	.attr("font-size", "12px")
	.attr("fill", "#404040")
	.text("The parameters change yearly for Station 1 - Tiburon");
		
//Initiate Legend	
var legend = svg.append("g")
	.attr("class", "legend")
	.attr("height", 100)
	.attr("width", 200)
	.attr('transform', 'translate(90,20)') 
	;
	//Create colour squares
	legend.selectAll('rect')
	  .data(LegendOptions)
	  .enter()
	  .append("rect")
	  .attr("x", w - 65)
	  .attr("y", function(d, i){ return i * 20;})
	  .attr("width", 10)
	  .attr("height", 10)
	  .style("fill", function(d, i){ return colorscale(i);})
	  ;
	//Create text next to squares
	legend.selectAll('text')
	  .data(LegendOptions)
	  .enter()
	  .append("text")
	  .attr("x", w - 52)
	  .attr("y", function(d, i){ return i * 20 + 9;})
	  .attr("font-size", "11px")
	  .attr("fill", "#737373")
	  .text(function(d) { return d; })
	  ;	
