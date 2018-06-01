function gridAnimation1() {
	var x = document.getElementById("bell");
	var y = document.getElementById("linkedin");
    setTimeout(function(){ 
    	x.style.display = "none";
    	y.style.transform = "rotate(10deg)"
    	gridAnimation2();
    	 }, 1000);
}
function gridAnimation2() {
	var x = document.getElementById("bell");
	var y = document.getElementById("linkedin");
    setTimeout(function(){ 
    	x.style.display = "block";
    	y.style.transform = "rotate(-10deg)"
    	gridAnimation1();
    	 }, 1000);
}
function githubAnimation() {
    var elem = document.getElementById("github"); 
    var margin = 80;
    var height = 50;
    function frame() {
        if (margin == 35) {
            clearInterval(id);
        } else {
            margin--; 
            height = height + 2;
            elem.style.marginLeft = margin + '%';
            elem.style.height = height + 'px';  
        }
    }
    var id = setInterval(frame, 50);
    setTimeout(function(){
    	githubAnimation();
    },4000)
}