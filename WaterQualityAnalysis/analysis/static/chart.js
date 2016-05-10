function chart(modaldivid, phpfile, parameter, sign, floatingPoint, safevalue) {
    console.log("phpfile: "+ phpfile);
    var margin = {top: 10, right: 91, bottom: 100, left: 50},
        margin2 = {top: 430, right: 91, bottom: 20, left: 50},
        width = 960 - margin.left - margin.right,
        height = 500 - margin.top - margin.bottom,
        height2 = 500 - margin2.top - margin2.bottom;

    // 2014-11-01T00:00:00Z
//    var parseDate = d3.time.format("%Y-%m-%dT%H:%M:%SZ").parse,

    var parseDate = d3.time.format("%Y-%m-%d").parse,
        bisectDate = d3.bisector(function (d) {
            return d.date;
        }).left,
        formatDate = d3.time.format("%d-%b-%y"),
        formatValue = d3.format(floatingPoint),
        formatData = function (d) {
            return formatValue(d) + " " + sign;
        };


    var x = d3.time.scale().range([0, width]),
        x2 = d3.time.scale().range([0, width]),
        y = d3.scale.linear().range([height, 0]),
        y2 = d3.scale.linear().range([height2, 0]);

    var xAxis = d3.svg.axis().scale(x).orient("bottom").ticks(d3.time.months, 1).tickFormat(d3.time.format("%m/%y")),
        xAxis2 = d3.svg.axis().scale(x2).orient("bottom").ticks(d3.time.months, 1).tickFormat(d3.time.format("%m/%y")),
        yAxis = d3.svg.axis().scale(y).orient("left");

    var yGridlines = d3.svg.axis().scale(y).orient("left").tickSize(-width, 0, 0).tickFormat("");


//    var xAxis = d3.svg.axis().scale(x).orient("bottom"),
//    xAxis2 = d3.svg.axis().scale(x2).orient("bottom")

    //  console.log(xAxis.ticks);

    var brush = d3.svg.brush()
        .x(x2)
        .on("brush", brushed);

    var line = d3.svg.line()
        .interpolate("monotone")
        .x(function (d) {
            return x(d.date);
        })
        .y(function (d) {
            return y(d.value);
        });

    var line2 = d3.svg.line()
        .interpolate("monotone")
        .x(function (d) {
            return x2(d.date);
        })
        .y(function (d) {
            return y2(d.value);
        });

    var svg = d3.select(modaldivid).append("svg")
        .attr("width", width + margin.left + margin.right)
        .attr("height", height + margin.top + margin.bottom);


    svg.append("defs").append("clipPath")
        .attr("id", "clip")
        .append("rect")
        .attr("width", width)
        .attr("height", height);

    var focus = svg.append("g")
        .attr("class", "focus")
        .attr("transform", "translate(" + margin.left + "," + margin.top + ")");

    var context = svg.append("g")
        .attr("class", "context")
        .attr("transform", "translate(" + margin2.left + "," + margin2.top + ")");


//    d3.csv("data.csv", type, function(error, data) {
//    d3.csv(file, function (error, data) {

    //"php/sfbaypier17ado.php"
    var data = JSON.parse(phpfile);
        data.forEach(function (d) {
            d.date = parseDate(d.date);
            d.value = +d.value;
        });

        data.sort(function (a, b) {
            return a.date - b.date;
        });


        x.domain(d3.extent(data.map(function (d) {
            return d.date;
        })));
        y.domain([0, d3.max(data.map(function (d) {
            return d.value;
        }))]);
        x2.domain(x.domain());
        y2.domain(y.domain());

//        lineSvg.append("path")                                 // **********
//                .attr("class", "line")
//                .attr("d", line(data));

        focus.append("g")
            .call(yGridlines)
            .classed("gridline", true)
            .attr("transform", "translate(0,0)");

        focus.append("path")
            .datum(data)
            .attr("class", "line")
            .attr("d", line);

        focus.append("line")
            .attr("x1", x(data[0].date))
            .attr("y1", y(safevalue))
            .attr("x2", x(data[data.length - 1].date))
            .attr("y2", y(safevalue))
            .attr("stroke", "orangered");

        focus.append("text")
            .attr("transform", "translate(" + (width - 78) + "," + y(safevalue - 2) + ")")
            .attr("dy", ".35em")
            .attr("text-anchor", "start")
            .style("fill", "orangered")
            .text(function (d) {
                return "Safe Value = " + safevalue
            });


        focus.append("g")
            .attr("class", "x axis")
            .attr("transform", "translate(0," + height + ")")
            .call(xAxis);

        focus.append("g")
            .attr("class", "y axis")
            .call(yAxis)
            .append("text")
            .attr("x", 0)
            .attr("y", 0)
            .style("text-anchor", "middle")
            .attr("transform", "translate(-40," + height / 2 + ") rotate(-90)")
            .text(parameter);

        context.append("path")
            .datum(data)
            .attr("class", "line")
            .attr("d", line2);

        context.append("g")
            .attr("class", "x axis")
            .attr("transform", "translate(0," + height2 + ")")
            .call(xAxis2);

        context.append("g")
            .attr("class", "x brush")
            .call(brush)
            .selectAll("rect")
            .attr("y", -6)
            .attr("height", height2 + 7);

        var xy = focus.append("g")
            .attr("class", "xy")
            .style("display", "none");

//        xy.append("circle")
//                .attr("r", 4.5);
//
//        xy.append("text")
//                .attr("x", 9)
//                .attr("dy", ".35em");

        // append the x line
        xy.append("line")
            .attr("class", "x")
            .style("stroke", "blue")
            .style("stroke-dasharray", "3,3")
            .style("opacity", 0.5)
            .attr("y1", 0)
            .attr("y2", height);

        // append the y line
        xy.append("line")
            .attr("class", "y")
            .style("stroke", "blue")
            .style("stroke-dasharray", "3,3")
            .style("opacity", 0.5)
            .attr("x1", width)
            .attr("x2", width);

        // append the circle at the intersection
        xy.append("circle")
            .attr("class", "y")
            .attr("r", 4);

        // place the value at the intersection
        xy.append("text")
            .attr("class", "y1")
            .style("stroke", "white")
            .style("stroke-width", "3.5px")
            .style("opacity", 0.8)
            .attr("dx", 8)
            .attr("dy", "-.3em");
        xy.append("text")
            .attr("class", "y2")
            .attr("dx", 8)
            .attr("dy", "-.3em");

        // place the date at the intersection
        xy.append("text")
            .attr("class", "y3")
            .style("stroke", "white")
            .style("stroke-width", "3.5px")
            .style("opacity", 0.8)
            .attr("dx", 8)
            .attr("dy", "1em");
        xy.append("text")
            .attr("class", "y4")
            .attr("dx", 8)
            .attr("dy", "1em");

        focus.append("rect")
            .attr("class", "overlay")
            .attr("width", width)
            .attr("height", height)
            .style("fill", "none")
            .on("mouseover", function () {
                xy.style("display", null);
            })
            .on("mouseout", function () {
                xy.style("display", "none");
            })
            .on("mousemove", mousemove);

        function mousemove() {
            var x0 = x.invert(d3.mouse(focus.node())[0]),
                i = bisectDate(data, x0, 1),
                d0 = data[i - 1],
                d1 = data[i],
                d = x0 - d0.date > d1.date - x0 ? d1 : d0;


            xy.select("circle.y")
                .attr("transform",
                    "translate(" + x(d.date) + "," +
                    y(d.value) + ")");

            xy.select("text.y1")
                .attr("transform",
                    "translate(" + x(d.date) + "," +
                    y(d.value) + ")")
                .text(formatDate(d.date));

            xy.select("text.y2")
                .attr("transform",
                    "translate(" + x(d.date) + "," +
                    y(d.value) + ")")
                .text(formatDate(d.date));

            xy.select("text.y3")
                .attr("transform",
                    "translate(" + x(d.date) + "," +
                    y(d.value) + ")")
                .text(formatData(d.value));

            xy.select("text.y4")
                .attr("transform",
                    "translate(" + x(d.date) + "," +
                    y(d.value) + ")")
                .text(formatData(d.value));

            xy.select(".x")
                .attr("transform",
                    "translate(" + x(d.date) + "," +
                    y(d.value) + ")")
                .attr("y2", height - y(d.value));

            xy.select(".y")
                .attr("transform",
                    "translate(" + width * -1 + "," +
                    y(d.value) + ")")
                .attr("x2", width + width);
//            console.log(x0);
//            xy.attr("transform", "translate(" + x(d.date) + "," + y(d.value) + ")");
//            xy.select("text").text(formatData(d.value));

            //console.log(width,"+",height);
        }


    function brushed() {
        x.domain(brush.empty() ? x2.domain() : brush.extent());
        focus.select(".line").attr("d", line);
        focus.select(".x.axis").call(xAxis);
    }

//    function type(d) {
//        d.date = parseDate(d.date);
//        d.value = +d.value;
//        return d;
//    }
}