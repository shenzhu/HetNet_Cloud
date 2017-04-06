
/// </// <reference path="angular.js" />
var homeApp = angular.module("homeModule", []);

var preUrl = "http://127.0.0.1:8111"
var homeApp = angular.module("homeModule", []);
var homeController = function($scope, $http, $window, httpService) {

	var email = $window.sessionStorage.getItem("userEmail");
	console.log(email);
	$scope.email = email;

	$scope.homeView = "../home/main.html";

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

	// Init network visualization
	$scope.networkVisualizationInit = function() {

		httpService.getnetworks().then(function (response) {
			$scope.networklist = response["data"];
            }, function(response){console.log(response);});
		
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

    	Highcharts.chart('pieChart1', {
		    chart: {
		        plotBackgroundColor: null,
		        plotBorderWidth: null,
		        plotShadow: false,
		        type: 'pie'
		    },
		    title: {
		        text: 'Browser market shares January, 2015 to May, 2015'
		    },
		    tooltip: {
		        pointFormat: '{series.name}: <b>{point.percentage:.1f}%</b>'
		    },
		    plotOptions: {
		        pie: {
		            allowPointSelect: true,
		            cursor: 'pointer',
		            dataLabels: {
		                enabled: true,
		                format: '<b>{point.name}</b>: {point.percentage:.1f} %',
		                style: {
		                    color: (Highcharts.theme && Highcharts.theme.contrastTextColor) || 'black'
		                }
		            }
		        }
		    },
		    series: [{
		        name: 'Brands',
		        colorByPoint: true,
		        data: [{
		            name: 'Microsoft Internet Explorer',
		            y: 56.33
		        }, {
		            name: 'Chrome',
		            y: 24.03,
		            sliced: true,
		            selected: true
		        }, {
		            name: 'Firefox',
		            y: 10.38
		        }, {
		            name: 'Safari',
		            y: 4.77
		        }, {
		            name: 'Opera',
		            y: 0.91
		        }, {
		            name: 'Proprietary or Undetectable',
		            y: 0.2
		        }]
		    }]
		});
	};
};

var httpService = function($http, $log){

    this.getnetworks = function(){
        return $http({
            url: preUrl + "/getnetwork",
            method: "GET",
        });
    }
	
    this.getLocationParser = function(Longtitude, Latitude){
       return $http({
            url: "http://maps.googleapis.com/maps/api/geocode/json",
            method: "GET",
            params:{latlng: Longtitude+","+Latitude}
		});
		// .success(function(response){
        //     address=response["results"][0]["formatted_address"];
        //     });
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