angular.module('paperApp').controller('CreateCtrl',['$scope', 'BookstoreService',function($scope, BookstoreService) {
    $scope.forms = {};
    $scope.info = {
        keywords : [
            {name:'a', id:1},
            {name:'b', id:2},
            {name:'c', id:3}
        ]
    }
    $scope.setForm = function (formName, form) {
        $scope.forms[formName] = form;
    }
    $scope.formdata = {
        title: '',
        abstract: '',
        keywords: [],
        authors: []
    }
    $scope.isAuthorEditMode = false;
    $scope.newAuthorModel = {
        firstname: '',
        lastname: '',
        contact: '',
        organization: '',
        selected: false
    }
    function initializeAuthorModel(model) {
        model.firstname = '';
        model.lastname = '';
        model.contact = '';
        model.organization = '';
        model.selected = false;

    }

    $scope.toggleKeyword = function(id) {
        var idx = $scope.formdata.keywords.indexOf(id);
        if (idx > -1) {
            $scope.formdata.keywords.splice( idx, 1);
        } else {
            $scope.formdata.keywords.push(id);
        }
    }

    $scope.getKeywordsAsString = function () {
        var str = '';
        for ( var idx = 0; idx < $scope.formdata.keywords.length; idx++) {
            for (var idx2 = 0; idx2 < $scope.info.keywords.length; idx2++) {
                if ($scope.formdata.keywords[idx] == $scope.info.keywords[idx2].id) {
                    str += ',' + $scope.info.keywords[idx].name;
                }
            }
        }
        return str.substring(1);
    }

    $scope.toggleAuthorsAll = function(index) {
        var isAllSelected = true;
        var idx = 0;
        for( idx = 0; idx < $scope.formdata.authors.length; idx++) {
            if( $scope.formdata.authors[idx].selected == false) {
                $scope.formdata.authors[idx].selected = true;
                isAllSelected = false;
            }
        }
        if (isAllSelected) {
            for( idx = 0; idx < $scope.formdata.authors.length; idx++) {
                $scope.formdata.authors[idx].selected = false;
            }
        }
    }
    $scope.AddNewAuthor = function() {
        if ($scope.forms.mainForm.lastname.$valid &&
            $scope.forms.mainForm.firstname.$valid &&
            $scope.forms.mainForm.contact.$valid &&
            $scope.forms.mainForm.organization.$valid
            ) {
            $scope.formdata.authors.push(angular.extend({}, $scope.newAuthorModel));
            initializeAuthorModel($scope.newAuthorModel);
            $scope.forms.mainForm.$setPristine();
            angular.element('input[name="lastname"]').focus();
        }
    }
    $scope.EditAuthor = function(index) {
        $scope.isAuthorEditMode = true;
        $scope.editingAuthorIndex = index;
        angular.extend( $scope.newAuthorModel, $scope.formdata.authors[index])
    }
    $scope.DeleteSelectedAuthors = function() {
        if( confirm("Are you sure you want to delete seletcted authors?") ) {
            for (var idx = $scope.formdata.authors.length - 1; idx >= 0; idx--) {
                if ($scope.formdata.authors[idx].selected == true) {
                    $scope.formdata.authors.splice(idx, 1);
                }
            }
        }
    }
    $scope.DeleteAuthor = function (index) {
        if( confirm("Are you sure you want to delete this author?") ) {
            $scope.formdata.authors.splice(index, 1);
        }
    }
    $scope.DiscardAuthor = function () {
        $scope.isAuthorEditMode = false;
        initializeAuthorModel($scope.newAuthorModel);
    }
    $scope.SaveAuthor = function() {
        $scope.isAuthorEditMode = false;
        angular.extend( $scope.formdata.authors[$scope.editingAuthorIndex], $scope.newAuthorModel);
        initializeAuthorModel($scope.newAuthorModel);
    }

    $scope.PostPaper = function() {
        if($scope.formdata.title.trim() == "") {
            alert("Please enter paper title.");
            return;
        }
        if ($scope.formdata.keywords.length == 0) {
            alert("Please select keywords")
            return;
        }
        if ($scope.formdata.authors.length == 0) {
            alert("Please select authors.");
            return;
        }
        BookstoreService.createPaper($scope.formdata);
    }
}])