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
	  		if(this.reasons.indexOf(this.new_reason) === -1 && this.new_reason !== "") {
	  			this.reasons.push(this.new_reason);
	  			this.new_reason = "";
	  		}
	  	},
		addHuman() {
	  		this.people.push({
	  			name: "",
	  			adult: true,
	  			sex: "Муж"
	  		});
	  	},
		deleteHuman(index) {
	  		this.people.splice(index, 1);
		},
	  	offer() {
	  		let ok = true;
	  		if(this.reasons.length < 1) {
	  			this.$buefy.notification.open({
					duration: 3000,
					message: `Пожалуйста, укажите ваши цели`,
					position: 'is-bottom-right',
					type: 'is-info',
					hasIcon: true
				});
	  			ok = false;
	  		}
	  		for(let i = 0; i < this.reasons.length; i += 1) {
	  			if(this.reasons[i].name === "") {
	  				this.$buefy.notification.open({
						duration: 3000,
						message: `Пожалуйста, заполните имя путешественника №${i + 1}`,
						position: 'is-bottom-right',
						type: 'is-info',
						hasIcon: true
					});
	  				ok = false;
	  			}
	  		}
	  		if(ok === true) {
	  			for(let i = 0; i < this.people.length; i += 1) {
	  				if(this.people[i].sex === "Муж") {
	  					this.people[i].sex = "M";
					} else {
	  					this.people[i].sex = "F";
					}
				}
	  			let requestInfo = {
					...this.flight,
					travel_type: this.reasons,
					people: {
						count: this.people.length,
						tourists: this.people
					}
	  			};
	  			console.log(requestInfo);
	  			chrome.storage.sync.set({
					requestInfo
        		});
			}
	  	}
	  },
	  watch: {
	  	people_count(new_val, old_val) {
	  		console.log("people count changed", old_val, new_val);
	  	}
	  },
	  computed: {
	  	people_count() {
	  		return this.people.length;
		},
	  },
	  beforeCreate() {
			chrome.storage.sync.get("flights", res => {
				this.flight = res.flights.arr[0]; 	
  			console.log(res.flights.arr[0])
			})
	  }  
	})
}