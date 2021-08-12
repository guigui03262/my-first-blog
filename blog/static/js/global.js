$(function() {
	// Carregamento via AJAX simples
	$('#num_users').load('http://127.0.0.1:8000/num_users/');

	$('img').css('border', '2px dashed black');
	$('img').css('border-radius', '10%')


	$(document).ready(function(){
		$("#hide").click(function(){
    		$("p").hide();
    		alert("Escondendo");
  		});
  		$("#show").click(function(){
    		$("p").show();
  		});
	});

});	