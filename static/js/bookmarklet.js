(function(){
	var jquery_version = '3.3.1';
	var site_url = 'http://localhost:8000/';
	var static_url = site_url + 'static/';
	var min_width = 50;
	var min_height = 50;

	function bookmarklet(){
		// load css
		var css = jQuery('<link>');
		css.attr({
			href: static_url + 'css/bookmarklet.css?r=' + Math.floor(Math.random() * 9999999),
			rel: 'stylesheet',
			type: 'text/css'
		});
		jQuery('head').append(css);

		// load body

		var box_html = '<div id="bookmarklet"><a id="close" href="#">&times;</a>' + 
			'<h1>Select an image to bookmark:</h1>' + 
			'<div class="images"></div>' + 
			'</div>' ;

		jQuery('body').append(box_html);

		jQuery('#bookmarklet #close').click(function(){
			jQuery('#bookmarklet').remove()
		});

		if (window.location.hostname.search(/google/) !== -1){
			jQuery.each(jQuery('.rg_meta'), function(index, meta){
				var metaObject = JSON.parse(meta.textContent);

				jQuery('#bookmarklet .images').append(
					'<a href=""><img src="' +
					metaObject.ou +
					'"></a>'
				)
			})
		} else {
			jQuery.each(jQuery('img[src$="jpg"]'), function(index, image){
				if (jQuery(image).width() >= min_width && jQuery(image).height() >= min_width){
					url = jQuery(image).attr('src')
					jQuery('#bookmarklet .images').append(
						'<a href="#"><img src="' +
						url + 
						'" alt=""></a>'
					)
				}
			});
		}

		jQuery('#bookmarklet .images a').click(function(){
			image = jQuery(this).children('img').attr('src')
			jQuery('#bookmarklet').hide()

			window.open(site_url + 
				'images/create/?url=' +
				encodeURIComponent(image) +
				'&title=' +
				encodeURIComponent(jQuery('title').text()) ,
				'_blank')
				
		})


	};

	if (typeof window.jQuery != 'undefined'){
		bookmarklet();
	} else {
		var conflict = typeof window.$ != 'undefined';
		var script = document.createElement('script');
		script.setAttribute('src', 
			'http://ajax.googleapis.com/ajax/libs/jquery/' +
			jquery_version +
			'/jquery.min.js');
		document.getElementsByTagName('head')[0].appendChild(script);

		var attemps = 15;
		(function(){
			if (typeof window.jQuery == 'undefined'){
				if(--attemps > 0){
					window.setTimeout(arguments.callee, 250)
				} else {
					window.alert('something wrong with loading jquery');
				}
			} else {
				bookmarklet();
			}
		})()
	}



})()
