var alertApp = angular.module('alertApp', []);

alertApp.controller('AlertCtrl', function($scope, $http, $interval) {

  $scope.notOk = function(alert) {
    return alert.contacted_warn || alert.contacted_fail;
  };

  $scope.formatTime = function(timestamp) {
    var millis = Date.now()-timestamp*1000
    if (millis < 60 * 60 * 1000) {
        return Math.round(millis / 1000 / 60) + ' minute(s)';
    }
    if (millis < 24 * 60 * 60 * 1000) {
        return Math.round(millis / 1000 / 60 / 60) + ' hour(s)';
    }
    return Math.round(millis / 1000 / 60 / 60 / 24) + ' day(s)';
  };

  $scope.alerts = {};
  $scope.error = '';

  function loadAlerts() {
    $http.get('/api/alerts').
      success(function(data) {
        $scope.alerts = data['alerts'];
        $scope.lastChecked = data['last_checked'];
        $scope.error = '';
      }).
      error(function(data) {
        $scope.error = 'There was an error getting alerts.';
      });
  }

  loadAlerts();

  $interval(function() {
    loadAlerts();
  }, 60000);

});
