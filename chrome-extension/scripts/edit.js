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
				data = flight
				data.travel_type = ["sking" , "work"]
				data.people = {
					count: 3,
					tourists : [
	     	 		{
		        	sex: "male",
		        	adult: true
		      	},
	      		{
		        	sex: "female",
		        	adult: true
		      	},
	      		{
		        	sex: "male",
		        	adult: false
	      		}
    			]
				}
  			$.post("http://localhost:5000/build", JSON.stringify(flight))
  				.done(response => { console.log(response) })
  				.fail(() => { console.log("Fail!") }) 	
  			console.log(res.flights.arr[0])
			})
	  }  
	})
}