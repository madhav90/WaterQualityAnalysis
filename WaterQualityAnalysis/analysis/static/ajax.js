function getData(stationName)
{
	//make db connection and get latlng and show pointers
	$.ajax({
		url : '127.0.0.1:8000/getSensorData',
		type : 'GET',
		data :{
			"station" : stationName,
		},
		dataType: 'json',
		success : function(data) {
				console.log("success in data:"+ data);
		},
		error : function(jqXHR, textStatus, errorThrown) {
			console.log('error here' + textStatus + "" + errorThrown);
		}
	});
}