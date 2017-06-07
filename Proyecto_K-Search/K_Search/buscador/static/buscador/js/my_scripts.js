$(document).ready(function(){

    var select1 = $(".contenidos");
    var select2 = $(".imagenes");
    var seccion_image1 = $("#seccion-option1");
    var seccion_image2 = $("#seccion-option2");
    var urls_form = document.urls_a_extraer;

    var giro1 = true;
    var giro2 = true;

    var input_search = $('#search');
	var boton_search = $("#btn-search");


	// Se clickea al cargar la pagina
	setTimeout(function() {
        $(".seccion-extraccion-imagenes").trigger('click');
    },100);


    /*
    $('.grid').masonry({
	  // options
	  itemSelector: '.grid-item',
	  columnWidth: 200
	});

	input_search.keyup(function(e){
		if(e.keyCode == 13){
			if(input_search.val()){
				boton_search.click();
			}
		}
	});

	$(".seccion-extraccion-imagenes").trigger("click");
	
	*/


	$("#btn_contenidos").on("click",function(){

		var checked = $("#urls_a_extraer input:checked").length > 0;

	    if (!checked){
	        alert("Selecciona al menos una de las paginas para extraer contenidos!");
	    }
	    else{
	    	$(this).prop("disabled", true);
			urls_form.submit();
	    }
	});


	$('.grid-item').on("click",function(){

		var div_id = (parseInt($(this).attr("id"))).toString();
		var clase = $(this).attr("class");
		var opt;

		if(clase == "grid-item con-sombrita cont"){
			opt = select1.find('option[value="'+ div_id +'"]');
		}
		else{
			opt = select2.find('option[value="'+ div_id +'"]');
		}

		if (opt.prop("selected")){
				opt.prop("selected",false)
            	.end()
            		.trigger("change");
            	$(this).css({"border": "2px solid #333", "transition": "border 0.2s linear"});
		}
		else{
			opt.prop("selected",true)
            	.end()
            		.trigger("change");
            $(this).css({"border": "4px solid blue", "transition": "border 0.2s linear"});
		}

	});


	$(".seccion-extraccion-contenidos").on("click",function(){

		$(".div-contenidos").fadeToggle();

		if(giro1){
			seccion_image1.css({"-webkit-transform":"rotate(90deg)", "transition": "-webkit-transform 0.3s ease"});
			giro1 = false;
			console.log("false");
		}
		else{
			seccion_image1.css({"-webkit-transform":"rotate(0deg)", "transition": "-webkit-transform 0.3s ease"});
			giro1 = true;
			console.log("true");
		}

		

	});



	$(".seccion-extraccion-imagenes").on("click",function(){

		$(".div-imagenes").fadeToggle();

		if(giro2){
			seccion_image2.css({"-webkit-transform":"rotate(90deg)", "transition": "-webkit-transform 0.3s ease"});
			giro2 = false;
		}
		else{
			seccion_image2.css({"-webkit-transform":"rotate(0deg)", "transition": "-webkit-transform 0.3s ease"});
			giro2 = true;
		}

	});




});