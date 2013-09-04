$(document).ready(function() { 
    
    $("[rel=tooltip]").tooltip();
    
    bubblesMain(new Object({
		  type : 'radial',
		  revolve : 'center',
		  minSpeed : 100,
		  maxSpeed : 600,
		  minSize : 35,
		  maxSize : 150,
		  num : 120,
          colors : new Array('#FFC847','#FF6047','#41B6D7')
	}));
    
});