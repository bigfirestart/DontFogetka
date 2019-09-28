$(document).ready(function() {
	startVue();
});

function startVue() {
	var app = new Vue({
	  el: '#app',
	  data: {
	    message: 'Hello Vue!',
	  	flight: null,
	  	predictions: null,
	  },
	  methods: {
	  },
	  beforeCreate() {
			chrome.storage.sync.get("flights", res => {
				flight = res.flights.arr[0];
  			$.post("localhost:5000/build", flight, response => {
  				console.log(response);
  			})	
  			console.log(res.flights.arr[0])
			})
	  }  
	})
}