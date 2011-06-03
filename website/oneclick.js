/*
One click
by @kennydude
*/
$(document).ready(function(){
	$(".oneclick").click(function(){
		popUp("installer.html?" + $(this).attr("href"));
		return false;
	});
});

function popUp(URL) {
day = new Date();
id = day.getTime();
eval("page" + id + " = window.open(URL, '" + id + "', 'toolbar=0,scrollbars=0,location=0,statusbar=0,menubar=0,resizable=0,width=500,height=300,left = 440,top = 362');");
}
