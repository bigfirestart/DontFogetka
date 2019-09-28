$(document).ready(function() {
	startVue();
});

function startVue() {
	var app = new Vue({
	  el: '#app',
	  data: {
	    message: 'Hello Vue!',
	  	flight: null,
	  },
	  methods: {
	  },
	  beforeCreate() {
			chrome.storage.sync.get("flights", res => {
				this.flight = res.flights.arr[0];
  			console.log(res.flights.arr[0])
			})
	  }  
	})
}