(function(){
	if (window.myBookmarklet !== undefined ){
		myBookmarklet();
	} else {
		var script = document.createElement('script');
		script.src = 'http://localhost:8000/static/js/bookmarklet.js?r=' + Math.floor(Math.random() * 99999999999999);
		document.body.appendChild(script);
	}
})()
