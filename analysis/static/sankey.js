google.charts.load("current", {packages:["sankey"]});
  google.charts.setOnLoadCallback(drawChart);
   function drawChart() {
    var data = new google.visualization.DataTable();
    data.addColumn('string', 'From');
    data.addColumn('string', 'To');
    data.addColumn('number', 'Weight');
    data.addRows([

       [ 'Water Quality', 'Dissolved Oxygen', 5 ],
       [ 'Water Quality', 'Turbity', 5 ],
       [ 'Water Quality', 'Chlorophyll', 5 ],
       [ 'Water Quality', 'Alkalinity', 5 ],
       [ 'Water Quality', 'Nitrate', 1 ],
       [ 'Dissolved Oxygen', 'Pressure', 2 ],
       [ 'Dissolved Oxygen', 'Salinity', 2 ],
       [ 'Dissolved Oxygen', 'Temperature', 2 ],


       [ 'Turbity', 'Clarity', 2 ],
       [ 'Turbity', 'Total suspended solids', 2 ],
       [ 'Chlorophyll', 'Temperature', 2 ],
       [ 'Chlorophyll', 'Sunlight', 2 ],

       [ 'Alkalinity', 'Ph', 2 ],
       [ 'Alkalinity', 'Temperature', 2 ],


    ]);

    // Set chart options
    var options = {
      width: 600,
    };

    // Instantiate and draw our chart, passing in some options.
    var chart = new google.visualization.Sankey(document.getElementById('sankey_multiple'));
    chart.draw(data, options);
   }