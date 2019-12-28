var mytrack = document.getElementById('mytrack')
var playButton = document.getElementById('playButton')
var muteButton = document.getElementById('muteButton')
//var downButton = document.getElementById('downButton')
var fullButton = document.getElementById('fullButton')

mytrack.addEventListener("dblclick",function(){
      if(window.outerWidth >= screen.availWidth){
    mytrack.requestFullscreen();
  }
})
mytrack.addEventListener('click',function(){
    if(window.outerWidth >= screen.availWidth) {
        if(!mytrack.paused && !mytrack.ended){
            mytrack.pause();
        }  else {
            mytrack.play();
        }
    }
})
var duration = document.getElementById('fullDuration')
var currentTime = document.getElementById('currentTime')

//document.getElementById("abc").href = mytrack.src;
//downButton.addEventListener('click',function () {
//  window.open(mytrack.src)
//} ,false)


fullButton.addEventListener('click',function(){
  if (mytrack.requestFullscreen) {
    mytrack.requestFullscreen();
  } else if (mytrack.exitFullscreen) {
    mytrack.exitFullscreen();
  }
})
var bar = document.getElementById('progressBar')
var allbar = document.getElementById('defaultBar')
barsize =  890
allbar.addEventListener('click',changetime,false)/*
allbar.addEventListener('toggle',changetime,false)*/
// var hours
// var minute
// var sec
var juicePos
var juicePo
mytrack.addEventListener('timeupdate',function(){
  juicePos = parseInt(mytrack.currentTime)
  juicePo = mytrack.currentTime / mytrack.duration;
  bar.style.width = juicePo * 100 + '%';
  if (juicePos >= 3600) {
   var hours = (mytrack.currentTime/60)/60
   var minute = (hours%1)*60
   var sec = parseInt((minute%1)*60)
   currentTime.innerHTML = parseInt(hours) +":" + parseInt(minute) + ":" + sec
  } else{
     minute = parseInt(mytrack.currentTime/60)
     sec = parseInt(mytrack.currentTime%60)
     currentTime.innerHTML =  minute + ":" + sec
  }
})
var hou
var minu
var secodn
var dud





mytrack.onpause = function () {
  playButton.style.backgroundImage = 'url(/static/svg/play.svg)';
}
mytrack.onplay = function () {
  playButton.style.backgroundImage = 'url(/static/svg/pause.svg)';
}
function check() {
  if (mytrack.muted == true) {
    muteButton.style.backgroundImage = 'url(/static/svg/mute.svg)'
  }
  if (mytrack.muted == false) {
    muteButton.style.backgroundImage = 'url(/static/svg/speaker.svg)'
  }
}
var f = setInterval(check,500)

function mute() {
  if (mytrack.muted == true) {
    mytrack.muted = false
    muteButton.style.backgroundImage = 'url(/static/svg/speaker.svg)';
  } else {
    mytrack.muted = true
    muteButton.style.backgroundImage = 'url(/static/svg/mute.svg)';
  }
}
muteButton.addEventListener('click',mute,false)
function playorPause(){
  calc()
  if(!mytrack.paused && !mytrack.ended){
    mytrack.pause();
    playButton.style.backgroundImage = 'url(/static/svg/play.svg)'; /* --------------------------------------   IF SOME THING WENT WRONG DELETE THOSE --------------------------*/
  }
  else {
    mytrack.play();
    playButton.style.backgroundImage = 'url(/static/svg/pause.svg)';/* --------------------------------------   IF SOME THING WENT WRONG DELETE THOSE --------------------------*/
  }
}
playButton.addEventListener('click',playorPause,false)

function changetime(e) {
  var mousex = e.pageX - allbar.offsetLeft;
  var newtime = mousex*(mytrack.duration/barsize)
  mytrack.currentTime = newtime
}

function calc() {
  dud = parseInt(mytrack.duration)
    if (dud >= 3600) {
   hou = (mytrack.duration/60)/60
   minu = (hou%1)*60
   secodn = parseInt((minu%1)*60)
   duration.innerHTML = parseInt(hou) +":" + parseInt(minu) + ":" + secodn
  } else{
     minu = mytrack.duration/60;
     secodn = parseInt(mytrack.duration % 60)
     console.log(secodn);
     duration.innerHTML =  parseInt(minu) + ":" + secodn
  }
}