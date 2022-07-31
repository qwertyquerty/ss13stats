var time_window = "DAY"
var stats_charts = [];

function set_time_window(window) {
	$(`#button-time-window-${time_window}`).removeClass("btn-primary");
	time_window = window;
	$(`#button-time-window-${time_window}`).addClass("btn-primary");

	clear_all_charts();
	update_all_charts();
}

function clear_all_charts() {
	for (index in stats_charts) {
		stats_charts[index].clear();
	}
}

function update_all_charts() {
	for (index in stats_charts) {
		stats_charts[index].update();
	}
}

$(document).ready(function() {
	setInterval(update_all_charts, 60 * 1000);
})

class SS13StatsChart {
	static chart_type = "line";
	static trend_line = true;
	static value_key = "value";

	constructor(canvas_id, title, endpoint) {
		this.canvas_id = canvas_id;
		this.title = title;
		this.endpoint = endpoint;

		let chart_options = {
			type: this.constructor.chart_type,
			data: {
				labels: [],
				datasets: [{
					label: title,
					data: [],
					borderColor: "#00ff00aa",
					borderWidth: 2
				}]
			},
			options: {
				responsive: true,
				scales: {
					x: {
						ticks: {
							display: true
						}
				   }
				}
			}
		}

		if (this.constructor.trend_line) {
			chart_options.data.datasets[0].trendlineLinear = {
				style: "#ff0000aa",
				lineStyle: "dotted",
				width: 2
			}
		}

		this.chart = new Chart(document.getElementById(this.canvas_id), chart_options);

		this.update();

		stats_charts.push(this);
	}

	update() {
		var stats_chart = this; // omg i love js scope

		$.getJSON(this.generate_endpoint(), function(data) {
			stats_chart.load_data(data);
		})
	}

	load_data(data) {
		this.chart.data.labels = data.map(entry => this.format_timestamp(entry.timestamp));
		this.chart.data.datasets[0].data = data.map(entry => entry[this.constructor.value_key]);
		this.chart.update();
	}

	format_timestamp(timestamp) {
		var date = new Date(timestamp + 'Z'); // Z indicates UTC

		if (time_window == "DAY") {
			return date.toLocaleTimeString('en-US', {
				hourCycle: 'h23'
			}).slice(0, -3);
		} else if (time_window == "WEEK") {
			return date.toLocaleString('en-US', {
				hourCycle: 'h23'
			}).slice(0, -3).replace(",", "");
		} else if (time_window == "MONTH") {
			return date.toLocaleDateString('en-US', {timeZone: "UTC"});
		} else if (time_window == "YEAR") {
			return date.toLocaleString('en-US', { month: 'long', timeZone: "UTC"});
		} else if (time_window == "ALL") {
			return date.getUTCFullYear();
		}
	}

	clear() {
		this.chart.data.labels = [];
		this.chart.data.datasets[0].data = [];
		this.chart.update();
	}

	generate_endpoint() {
		var grouping;
		var limit;

		if (time_window == "DAY") {
			limit = 144;
		} else if (time_window == "WEEK") {
			grouping = "HOUR";
			limit = 168;
		} else if (time_window == "MONTH") {
			grouping = "DAY";
			limit = 30;
		} else if (time_window == "YEAR") {
			grouping = "MONTH";
			limit = 12;
		} else if (time_window == "ALL") {
			grouping = "YEAR"
		}

		var generated_endpoint = this.endpoint;

		if (grouping) {
			generated_endpoint += `&grouping=${grouping}`;
		}

		if (limit) {
			generated_endpoint += `&limit=${limit}`;
		}

		return generated_endpoint;
	}
}

class SS13ServerStatsChart extends SS13StatsChart {
	static value_key = "player_count";
}

class SS13GlobalWeekdayAverages extends SS13StatsChart {
	static chart_type = "bar";
	static trend_line = false;
	static value_key = "value";

	generate_endpoint() {
		return this.endpoint;
	}

	format_timestamp(timestamp) {
		var date = new Date(timestamp + 'Z'); // Z indicates UTC
		return date.toLocaleString('en-US', {weekday: "long", timeZone: "UTC"});
	}
}

class SS13ServerWeekdayAverages extends SS13GlobalWeekdayAverages {
	static value_key = "player_count";
}
