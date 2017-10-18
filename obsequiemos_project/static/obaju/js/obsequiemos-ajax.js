/**
 * Created by alonso on 10/30/16.
 */
$(document).ready(function() {
        // JQuery code to be added in here.

        $.ajaxSetup({ cache: true });
          $.getScript('//connect.facebook.net/es_CL/sdk.js', function(){
            FB.init({
              appId: '2037530789806710',
              version: 'v2.8' // or v2.0, v2.1, v2.2, v2.3
            });
            $('#loginbutton,#feedbutton').removeAttr('disabled');
            FB.getLoginStatus(updateStatusCallback);
          });


        $('.regalar').click(function(event) {
            var id_postulation = event.target.id;
            $.get('/ganador/', {id_postulation:id_postulation}, function(data){
                    var aux = data;
                    console.log(aux);
            });
        });

        $('.seleccionar').click(function(event) {
            var id_postulation = event.target.id;
            $.get('/seleccionado/', {id_postulation:id_postulation}, function(data){
                    var aux = data;
                    console.log(aux);
            });
        });

        $('#like').click(function(event) {
            var postid;
            postid = $(this).attr("data-postid");
            $.get('/like_post/', {post_id: postid}, function(data){
                    $('#like_count').html(data);
                    $('#likes').hide();
            });
        });



        $('#id_region').change(function(event) {
            var region;
            region = $(this).find(':selected').val();
            if(region)
            {
                $.ajax({
                    type:'GET',
                    url: '/get_provincias/',
                    dataType:'JSON',
                    data: {
                        'name_region': region,
                    },
                    "success": function(data){
                        $("#id_provincia").html("");
                        $("#id_comuna").html("");
                        var no_select = "---------";
                        $("#id_provincia").append('<option value="' + no_select + '">' + no_select + '</option>');
                        $("#id_comuna").append('<option value="' + no_select + '">' + no_select + '</option>');
                        $.each(data, function(key, val){
                          $("#id_provincia").append('<option value="' + val.provincia_name + '">' + val.provincia_name + '</option>');
                        })
                    },
                    "error": function(req, status,err){
                        console.log('Algo anda mal',status,err,req);
                        alert('error; '+ eval(err));
                    }
                });
            }
            else
            {
                $("#id_provincia").html("<option value='' selected='selected'>---------</option>");
                $("#id_provincia").trigger("change");
            }

            $('#id_provincia').show();
            return false;
        });

        $('#id_provincia').change(function(event) {
            var provincia;
            provincia = $(this).find(':selected').val();
            if(provincia)
            {
                $.ajax({
                    type:'GET',
                    url: '/get_comunas/',
                    dataType:'JSON',
                    data: {
                        'name_provincia': provincia,
                    },
                    "success": function(data){
                        $("#id_comuna").html("");
                        var no_select = "---------";
                        $("#id_comuna").append('<option value="' + no_select + '">' + no_select + '</option>');
                        $.each(data, function(key, val){
                          $("#id_comuna").append('<option value="' + val.id + '">' + val.comuna_name + '</option>');
                        })
                    },
                    "error": function(req, status,err){
                        console.log('Algo anda mal',status,err,req);
                        alert('error; '+ eval(err));
                    }
                });
            }
            else
            {
                $("#id_comuna").html("<option value='' selected='selected'>---------</option>");
                $("#id_comuna").trigger("change");
            }
        $("#id_comuna").show();
        return false;
        });

        $('#id_category').change(function(event) {
            var category;
            category = $(this).find(':selected').val();
            if(category)
            {
                $.ajax({
                    type:'GET',
                    url: '/get_subcategories/',
                    dataType:'JSON',
                    data: {
                        'name_category': category,
                    },
                    "success": function(data){
                        $("#id_subcategory").html("");
                        var no_select = "---------";
                        $("#id_subcategory").append('<option value="' + no_select + '">' + no_select + '</option>');
                        $.each(data, function(key, val){
                          $("#id_subcategory").append('<option value="' + val.id + '">' + val.name_subcategory + '</option>');
                        })
                    },
                    "error": function(req, status,err){
                        console.log('Algo anda mal',status,err,req);
                        alert('error; '+ eval(err));
                    }
                });
            }
            else
            {
                $("#id_subcategory").html("<option value='' selected='selected'>---------</option>");
                $("#id_subcategory").trigger("change");
            }
        $("#id_subcategory").show();
        return false;

        });

        $('.notificacion').click(function(event) {
            var notificiacionid;
            notificiacionid = event.target.id;
            $.get('/read_notificacion/', {notificiacionid: notificiacionid}, function(data){

            });
        });

        /**
         * Este script de javascript permite trabajar transparentemente solicitudes que requieren
         * protección del token CSRF por medio de AJAX JQUERY.
         * Esto te permitirá hacer solcitudes a web Services de Django por medio de AJAX Jquery.
         * Para utilizarlo basta con integrar el archivo DjangoAjax.js en tu directorio de JS  y hacer referencia a él en tus templates
         * que requieren del uso de AJAX por POST o algún otro que requiera el token CSRF.
         * Este script está basado en la documentación oficial de Django https://docs.djangoproject.com
         */

        $(function(){
            //Obtenemos la información de csfrtoken que se almacena por cookies en el cliente
            var csrftoken = getCookie('csrftoken');

            //Agregamos en la configuración de la funcion $.ajax de Jquery lo siguiente:
            $.ajaxSetup({
                            beforeSend: function(xhr, settings) {
                                if (!csrfSafeMethod(settings.type) && sameOrigin(settings.url)) {
                                    // Send the token to same-origin, relative URLs only.
                                    // Send the token only if the method warrants CSRF protection
                                    // Using the CSRFToken value acquired earlier
                                    xhr.setRequestHeader("X-CSRFToken", csrftoken);
                                }
                            }
            });

        function sameOrigin(url) {
            // test that a given url is a same-origin URL
            // url could be relative or scheme relative or absolute
            var host = document.location.host; // host + port
            var protocol = document.location.protocol;
            var sr_origin = '//' + host;
            var origin = protocol + sr_origin;
            // Allow absolute or scheme relative URLs to same origin
            return (url == origin || url.slice(0, origin.length + 1) == origin + '/') ||
                (url == sr_origin || url.slice(0, sr_origin.length + 1) == sr_origin + '/') ||
                // or any other URL that isn't scheme relative or absolute i.e relative.
                !(/^(\/\/|http:|https:).*/.test(url));
        }

        // usando jQuery
        function getCookie(name) {
            var cookieValue = null;
            if (document.cookie && document.cookie != '') {
                var cookies = document.cookie.split(';');
                for (var i = 0; i < cookies.length; i++) {
                    var cookie = jQuery.trim(cookies[i]);
                    // Does this cookie string begin with the name we want?
                    if (cookie.substring(0, name.length + 1) == (name + '=')) {
                        cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                        break;
                    }
                }
            }
            return cookieValue;
        }


            function csrfSafeMethod(method) {
                // estos métodos no requieren CSRF
                return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
            }
        });
        /*Fin script CSRF TOKEN*/

        window.fbAsyncInit = function() {
        FB.init({
          appId      : '2037530789806710',
          xfbml      : true,
          version    : 'v2.8'
        });
      };

      (function(d, s, id){
         var js, fjs = d.getElementsByTagName(s)[0];
         if (d.getElementById(id)) {return;}
         js = d.createElement(s); js.id = id;
         js.src = "//connect.facebook.net/es_CL/sdk.js";
         fjs.parentNode.insertBefore(js, fjs);
       }(document, 'script', 'facebook-jssdk'));

});

