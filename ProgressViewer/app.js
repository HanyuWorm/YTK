var app = angular.module('app', ['ngSanitize', 'ngRoute']);
var fs = require('fs');
var spawn = require('child_process').spawn;
const { exec } = require('child_process');

app.config(function($routeProvider) {
    $routeProvider
    .when("/", {
        templateUrl : "main.html"
    })
    .when("/progress", {
        templateUrl : "progress.html"
    })
    .when("/green", {
        templateUrl : "green.htm"
    })
    .when("/blue", {
        templateUrl : "blue.htm"
    });
});
state = {}
state.project = ''

app.controller('ProjectController', function($scope, $location) {
    $scope.projects = [];
    $scope.detail = function(project) {
        state.project = project;
        $location.url('/progress');
    }
    fs.readdir('./../data', function(err, items) {
        for (var i=0; i<items.length; i++) {
            item = items[i];
            $scope.projects.push(item);
        }
        $scope.$apply();
    });
})
app.controller('ProgressController', function($scope, $location) {
    $scope.project = {};
    $scope.project.name = state.project;
    $scope.progress = []
    $scope.percent = {};

    $scope.count = {};
    $scope.count.crawler = 0;
    $scope.count.image = 0;
    $scope.count.video = 0;
    $scope.count.youtube_upload = 0;
    $scope.count.audio = 0;

    fs.readFile(`./../config.json`, 'utf8', function(err, data) {
        $scope.project = JSON.parse(data)[state.project]
        console.log($scope.project)
        $scope.$apply();
        
        $scope.progress = get_progress(state.project, $scope.project.start_chapter, $scope.project.lastest_chapter, $scope.project.chapter_per_video);
        // console.log($scope.progress);
        number_videos = Math.ceil($scope.project.lastest_chapter/$scope.project.chapter_per_video );
        console.log(number_videos)
        console.log($scope.count.crawler)
        $scope.percent.crawler = ($scope.count.crawler*100 / number_videos).toFixed(2);
        $scope.percent.audio = ($scope.count.audio*100 / number_videos).toFixed(2);
        $scope.$apply();
    });
    

    
    


    get_progress = function(project, start_chapter, lastest_chapter, chapter_per_video) {
        listdir = fs.readdirSync('./../data/' + project);
        arr = []

        for(let i = 1; i<= lastest_chapter; i+=10) {
            item = {}
            start = i;
            end = i + 9 <=lastest_chapter ? i+9 : lastest_chapter;
            item.chapter = `chapter ${start} - ${end}`

            item.crawler = '';
            
            for(let chapter = start; chapter <= end; chapter ++)
            {
                if(listdir.indexOf(('chuong-'+chapter+'.txt')) >= 0 && listdir.indexOf(('chuong-'+chapter+'.title') >= 0)) {
                    item.crawler += '<span class="text-success font-10" >' + chapter + '</span> ';
                    $scope.count.crawler += 1;
                } else {
                    item.crawler += '<span class="text-danger">' + chapter + '</span> ';
                }
            }

            // audio one chapter
            item.audio = '';
            
            for(let chapter = start; chapter <= end; chapter ++)
            {
                if(listdir.indexOf(('chuong-'+chapter)) >= 0 && fs.readdirSync('./../data/' + project + '/chuong-'+chapter).indexOf('full.mp3') >= 0) {
                    item.audio += '<span class="text-success font-10" >' + chapter + '</span> ';
                    $scope.count.audio += 1;
                } else {
                    item.audio += '<span class="text-danger">' + chapter + '</span> ';
                }
            }

            
            arr.push(item);
        }
        return arr;
        
    }
});



app.controller('HelloController', function($scope) {
    $scope.inputs = [];
    $scope.voices = ['male', 'female', 'hatieumai', 'ngoclam', 'leminh'];

    $scope.result = '>';
    $scope.voice = "female";
    $scope.speed = 0;
    $scope.input = "input";
    $scope.prosody = false;

    fs.readdir('./app', function(err, items) {
        for (var i=0; i<items.length; i++) {
            item = items[i];
            tmp = item.split('.');
            if(tmp[tmp.length - 1] == 'txt' && tmp[0] != 'help'){
                $scope.inputs.push(tmp[0]);
            }
        }
        $scope.$apply();
    });

    $scope.merge = function() {
        console.log('merge');
        var merge    = spawn('app.exe', ['merge', $scope.input], { cwd: "app" });
        console.log($scope.voice);
        console.log($scope.speed);
        console.log($scope.input);
        console.log($scope.prosody);

        $scope.result = '> merge';
        $scope.$apply();
        merge.stdout.on('data', function (data) {
            console.log('stdout: ' + data.toString());
            $scope.result += '<span class="text-success">' + data.toString().split('\n').join('<br/>') + '</span><br/>';
            $scope.$apply();
        });
        merge.stderr.on('data', function (data) {
            console.log('stderr: ' + data.toString());
            $scope.result += '<span class="text-danger">' + data.toString().split('\n').join('<br/>') + '</span><br/>';
            $scope.$apply();
        });
    }
    $scope.run_all = function() {

        console.log('run all');
        exec('cd app');
        var runall    = spawn('app.exe', ['run_all', $scope.input, $scope.voice, $scope.speed, $scope.prosody], { cwd: "app" });
        $scope.result = '> run all <br/>';
        runall.stdout.on('data', function (data) {
            console.log('stdout: ' + data.toString());
            $scope.result += '<span class="text-success"">' + data.toString().split('\n').join('<br/>') + '</span><br/>';
            $scope.$apply();
        });
        runall.stderr.on('data', function (data) {
            console.log('stderr: ' + data.toString());
            $scope.result += '<span class="text-danger">' + data.toString().split('\n').join('<br/>') + '</span><br/>';
            $scope.$apply();
        });
    }
});