$(document).ready(function() {
	startVue();
});

function startVue() {
	console.log(Buefy);
	Vue.use(Buefy);
	var app = new Vue({
	  el: '#app',
	  data: {
	    flight: null,
	    new_reason : "",
	    reasons: [],
	  	people_count: 1,
	  	people: [
	  		{
	  			name: "",
	  			adult: true,
	  			sex: "Муж"
	  		}
	  	],
	  	predictions: null,
	  },
	  methods: {
	  	addReason() {
	  		if(this.reasons.indexOf(this.new_reason) === -1) {
	  			this.reasons.push(this.new_reason);
	  		}
	  	},
	  	offer() {
	  		if(this.reasons.length < 1) {
	  			this.$buefy.notification.open({
            duration: 3000,
            message: `Пожалуйста, укажите ваши цели`,
            position: 'is-bottom-right',
            type: 'is-info',
            hasIcon: true
	        })
	  		}
	  		for(let i = 0; i < this.reasons.length; i += 1) {
	  			if(this.reasons[i].name === "") {
	  				this.$buefy.notification.open({
	            duration: 3000,
	            message: `Пожалуйста, заполните имя путешественника №${i + 1}`,
	            position: 'is-bottom-right',
	            type: 'is-info',
	            hasIcon: true
	        	})
	  			}
	  		}
	  	}
	  },
	  watch: {
	  	people_count(new_val, old_val) {
	  		if(new_val > old_val) {
		  		this.people.push({
		  			name: "",
		  			adult: true,
		  			sex: "Муж"
		  		})
	  		} else {
	  			this.people.pop()
	  		}
	  	}
	  },
	  beforeCreate() {
			chrome.storage.sync.get("flights", res => {
				this.flight = res.flights.arr[0]; 	
  			console.log(res.flights.arr[0])
			})
	  }  
	})
}