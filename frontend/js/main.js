
/// </// <reference path="angular.js" />
var homeApp = angular.module("homeModule", []);

var preUrl = "http://127.0.0.1:8111"
var homeApp = angular.module("homeModule", []);
var homeController = function($scope, $http, $window, httpService) {

	var email = $window.sessionStorage.getItem("userEmail");
	$scope.email = email;

	$scope.homeView = "../home/main.html";

	$scope.networkList;
	$scope.appdataList;


	// switch to main
	$scope.switchMain = function() {
		$scope.homeView ="../home/main.html";
		console.log("home executed");
	};

	// switch to network data
	$scope.switchNetworkData = function() {
		console.log("EXECUTED");
		$scope.homeView = "../home/networkData.html";
		console.log("2");
	};

	// switch to network visualization
	$scope.switchNetworkDataVisualization = function() {
		$scope.homeView = "../home/networkDataVisualization.html";
		console.log("net vis switched");
	};

	// switch to application data
	$scope.switchApplicationData = function() {
		$scope.homeView = "../home/applicationData.html";
	};

	// switch to application data visualization
	$scope.switchApplicationDataVisualization = function() {
		$scope.homeView = "../home/applicationDataVisualization.html";
	};

	// switch to system data
	$scope.switchSystemData = function() {
		$scope.homeView = "../home/systemData.html";
	};

	// switch to system data visualization
	$scope.switchSystemDataVisualization = function() {
		$scope.homeView = "../home/systemDataVisualization.html";
	};

	// Init network data
	$scope.networkDataInit = function() {

		var networkList = [];
		httpService.getnetworks().then(function (response) {
			console.log(response.data.networks);
			for (var i = 0; i < response.data.networks.length; i++) {
				var network = {
					"ssid": response.data.networks[i].ssid,
					"bandwidth": response.data.networks[i].bandwidth,
					"avgss": response.data.networks[i].avgss,
					"location": response.data.networks[i].location,
					"security": response.data.networks[i].security,
					"device_id": response.data.networks[i].device_id,
					"time": response.data.networks[i].time
				};
				networkList.push(network);
			}
			$scope.networkList = networkList;
		});
	};

	// Init application data
	$scope.applicationDataInit = function() {
		var appdataList = [];
		httpService.getappdata().then(function (response) {
			console.log(response.data.appdata);
			$scope.appdataList = response.data.appdata;
		});
	};

	// Init network visualization
	$scope.networkVisualizationInit = function() {

		httpService.getnetworks().then(function (response) {

		});
		
		console.log($scope.networklist);

		Highcharts.chart('barChart1', {
        	chart: {
            	type: 'column'
        	},
        	title: {
            	text: 'Distribution of Average Signal Strength in dB'
        	},
        	xAxis: {
            	//categories: ['Apples', 'Bananas', 'Oranges']
            	categories: ['-103.08707097',  '-99.54836933',  '-96.00966769',  '-92.47096605',
        	'-88.93226442',  '-85.39356278',  '-81.85486114',  '-78.31615951',
        	'-74.77745787',  '-71.23875623',  '-67.70005459']
        	},
        	yAxis: {
	            title: {
    	            text: 'Number of networks'
        	    }
        	},
        	series: [{
	            name: 'Number of networks',
    	        data: [1,  1,  1,  5,  4,  5,  9, 11,  5,  8]
	        }]
    	});

    	Highcharts.chart('barChart2', {
        	chart: {
            	type: 'column'
        	},
        	title: {
	            text: 'Distribution of Average Bandwidth in Mbit/s'
    	    },
        	yAxis: {
            	categories: ['35.02654303',  '38.73984845',  '42.45315388',  '46.1664593',
        	'49.87976473',  '53.59307015',  '57.30637557',  '61.019681',
        	'64.73298642',  '68.44629185',  '72.15959727']
        	},
        	xAxis: {
            	title: {
                	text: 'Number of networks'
            	}
        	},
        	series: [{
            	name: 'Number of networks',
            	data: [9,  4,  1,  6,  7,  7, 10,  3,  1,  2]
        	}]
    	});
	};

	// Init appdata visualization
	$scope.appdataVisualizationInit = function() {
		$.getJSON('https://www.highcharts.com/samples/data/jsonp.php?filename=usdeur.json&callback=?', function (data) {

    Highcharts.chart('appTimeSeries1', {
        chart: {
            zoomType: 'x'
        },
        title: {
            text: 'Upload Statistics by Chrome(in MB)'
        },
        subtitle: {
            text: document.ontouchstart === undefined ?
                    'Click and drag in the plot area to zoom in' : 'Pinch the chart to zoom in'
        },
        xAxis: {
            type: 'datetime'
        },
        yAxis: {
            title: {
                text: 'Upload'
            }
        },
        legend: {
            enabled: false
        },
        plotOptions: {
            area: {
                fillColor: {
                    linearGradient: {
                        x1: 0,
                        y1: 0,
                        x2: 0,
                        y2: 1
                    },
                    stops: [
                        [0, Highcharts.getOptions().colors[0]],
                        [1, Highcharts.Color(Highcharts.getOptions().colors[0]).setOpacity(0).get('rgba')]
                    ]
                },
                marker: {
                    radius: 2
                },
                lineWidth: 1,
                states: {
                    hover: {
                        lineWidth: 1
                    }
                },
                threshold: null
            }
        },

        series: [{
            type: 'area',
            name: 'upload',
            data: data
        }]
    });
});

		Highcharts.chart('appPieChart1', {
        chart: {
            plotBackgroundColor: null,
            plotBorderWidth: null,
            plotShadow: false,
            type: 'pie'
        },
        title: {
            text: 'Upload Statistics by Different Applications'
        },
        tooltip: {
            pointFormat: '{series.name}: <b>{point.percentage:.1f}%</b>'
        },
        plotOptions: {
            pie: {
                allowPointSelect: true,
                cursor: 'pointer',
                dataLabels: {
                    enabled: false
                },
                showInLegend: true
            }
        },
        series: [{
            name: 'Brands',
            colorByPoint: true,
            data: [{
                name: 'chrome',
                y: 56.33
            }, {
                name: 'youtube',
                y: 24.03,
                sliced: true,
                selected: true
            }, {
                name: 'hetnet',
                y: 10.38
            }, {
                name: 'com.google.android.talk',
                y: 4.77
            }, {
                name: 'com.google.uid.shared:10010',
                y: 0.91
            }, {
                name: 'com.kingouser.com',
                y: 0.2
            }]
        }]
    });

		Highcharts.chart('appPieChart2', {
        chart: {
            plotBackgroundColor: null,
            plotBorderWidth: null,
            plotShadow: false,
            type: 'pie'
        },
        title: {
            text: 'Download Statistics by Different Applications'
        },
        tooltip: {
            pointFormat: '{series.name}: <b>{point.percentage:.1f}%</b>'
        },
        plotOptions: {
            pie: {
                allowPointSelect: true,
                cursor: 'pointer',
                dataLabels: {
                    enabled: false
                },
                showInLegend: true
            }
        },
        series: [{
            name: 'Brands',
            colorByPoint: true,
            data: [{
                name: 'chrome',
                y: 46.33
            }, {
                name: 'youtube',
                y: 17.03,
                sliced: true,
                selected: true
            }, {
                name: 'hetnet',
                y: 15.38
            }, {
                name: 'com.google.android.talk',
                y: 12.77
            }, {
                name: 'com.google.uid.shared:10010',
                y: 3.91
            }, {
                name: 'com.kingouser.com',
                y: 4.58
            }]
        }]
    });
	};
};

var httpService = function($http){

    this.getnetworks = function(){
        return $http({
            url: preUrl + "/getnetwork",
            method: "GET",
        });
    }

    this.getappdata = function() {
    	return $http({
    		url: preUrl + "/getappdata",
    		method: "GET",
    	});
    }
	
    this.getLocationParser = function(Longtitude, Latitude){
       return $http({
            url: "http://maps.googleapis.com/maps/api/geocode/json",
            method: "GET",
            params:{latlng: Longtitude+","+Latitude}
		});
    }
    this.getLatestlocation = function(myemail){
        return $http({
            url: preUrl + "/location",
            method: "GET",
            params:{Email : myemail, sort: '-Time', limit: 1}
        });
    }
    this.getLatestnetwork = function(myemail){
        return $http({
            url: preUrl + "/network",
            method: "GET",
            params:{Email : myemail, sort: '-Time', limit: 1}
        });
    }
    this.getLastestSystemInfo = function(myemail){
        return $http({
            url: preUrl + "/system",
            method: "GET",
            params:{Email : myemail, sort: '-Time', limit: 1}
        });
    }
}

homeApp.controller("homeController", homeController);
homeApp.service("httpService", httpService);