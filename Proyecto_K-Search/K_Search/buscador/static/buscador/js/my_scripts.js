$(document).ready(function(){

    var select1 = $(".contenidos");
    var select2 = $(".imagenes");
    var select3 = $(".contenidos_ver");
    var select4 = $(".imagenes_ver");
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


    $("#login").hover(function() {
		$("#login-form").slideToggle();
	});


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


	$('.grid-item-ver').on("click",function(){

		var div_id = (parseInt($(this).attr("id"))).toString();
		var clase = $(this).attr("class");
		var opt;

		if(clase == "grid-item-ver con-sombrita cont"){
			opt = select3.find('option[value="'+ div_id +'"]');
		}
		else{
			opt = select4.find('option[value="'+ div_id +'"]');
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

	var change_select = false;


	$(".contenidos,.imagenes").on("change", function(ev, data){

		var num_selecciones1 = select1.val().length;
		var num_selecciones2 = select2.val().length;

		if (num_selecciones1 == 0 && num_selecciones2 == 0){

			change_select = false;
			$("#btn_save_contenidos").hide();
		}
		else{
			if(!change_select){
				change_select = true;
				$("#btn_save_contenidos").show();
			}
		}

    });



	$(".contenidos_ver,.imagenes_ver").on("change", function(ev, data){

		var num_selecciones1 = select3.val().length;
		var num_selecciones2 = select4.val().length;

		if (num_selecciones1 == 0 && num_selecciones2 == 0){

			change_select = false;
			$("#btn_save_contenidos").hide();
			$("#input-tags").hide();
		}
		else{
			if(!change_select){
				change_select = true;
				$("#btn_save_contenidos").show();
				$("#input-tags").show();
				// Aparecer boton añadir tag, editar y eliminar
			}
		}

    });




    $("#btn_save_contenidos").on("click",function(){

		var num_selecciones1 = select1.val().length;
		var num_selecciones2 = select2.val().length;

		if (num_selecciones1 == 0 && num_selecciones2 == 0){
			alert("Selecciona al menos un contenido para guardar!");
		}
	    else{
	    	$(this).prop("disabled", true);
			$("#seleccion_form").submit();
	    }
	});




	$(".delete").on("click",function(){

		var dominio = $(this).attr("id");

		$("#delete_id").val(dominio);
		$("#delete_form").submit();

	});

	// STARS CALIFICATION -----------------------------

	var options = {
        max_value: 5,
        step_size: 1,
        initial_value: 3,
    }

    var change = false;

    $(".rate").rate(options);

   	$(".rate").on("change", function(ev, data){
        if(!change){
        	change = true;
        	$("#btn_save").show();
        }

        var actual_val = $("#change_rating").val();
        $("#change_rating").val(actual_val+","+$(this).attr("id"));
    });

   	
    //$(".rate2").on("change", function(ev, data){
    //    console.log(data.from, data.to);
    //});

	// ------------------------------------------------

});