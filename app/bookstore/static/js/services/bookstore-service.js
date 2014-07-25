angular.module('paperApp').factory('BookstoreService',['$http', function( $http ){
    return {
        createPaper: function(paperInfo) {
            $http({
                method: 'POST',
                url:    '/api/v1/paper/',
                data:   paperInfo
            });
        }
    };

}]);