angular.module('paperApp').factory('BookstoreService',['$http', function( $http ){
    return {
        createPaper: function(paperInfo, callback) {
            var formdata = new FormData();
            for( var key in paperInfo) {
                if (typeof paperInfo[key] == 'object') {
                    formdata.append(key, JSON.stringify(paperInfo[key]));
                } else {
                    formdata.append(key, paperInfo[key]);
                }
            }
            return $http.post('/api/v1/paper/', formdata, {
                transformRequest: angular.identity,
                progress: callback
            });
        },
        getKeywords: function(success, error) {
            return $http.get('/api/v1/keyword/').
                success(function() {
                    if (success) {
                        success(arguments)
                    }
                }).
                error(function() {
                    if (error) {
                        error(arguments)
                    }
                });
        }
    };

}]);