// Initial chart setup
const chartOptions1 = {
    layout: {
        background: { type: 'solid', color: 'white' },
        textColor: 'black',
    },
    grid: {
        vertLines: {
            color: '#e1e1e1',
        },
        horzLines: {
            color: '#e1e1e1',
        },
    },
    crosshair: {
        mode: LightweightCharts.CrosshairMode.Normal,
    },
    timeScale: {
        visible: true,
        timeScale:true,
        timeVisible:true
    },
    width: document.getElementById('chart').clientWidth,
    height: document.getElementById('chart').clientHeight,
};



const chart = LightweightCharts.createChart(document.getElementById('chart'), chartOptions1);
const candlestickSeries = chart.addCandlestickSeries();


let autoUpdateInterval;

// Fetch data function
function fetchData(from_date,to_date,expiry_date,strike_price,option,timeframe,script_code) {
    console.log('hi',from_date,to_date,expiry_date,strike_price,option,timeframe,script_code)
    // fetch(`/api/data/${fromDate}/${toDate}/${expiryDate}/${strikePrice}/${option}/${timeframe}/${scriptCode}/${emaPeriod}/${rsiPeriod}/${interval}`)

    fetch(`/api/data/${from_date}/${to_date}/${expiry_date}/${strike_price}/${option}/${timeframe}/${script_code}`)
        .then(response => response.json())
        .then(data => {
            candlestickSeries.setData(data.candlestick);

            
        })
        .catch(error => {
            console.error('Error fetching data:', error);
        });
}

// Fetch NVDA data on page load with default timeframe (daily), EMA period (20) and RSI period (14)
window.addEventListener('load', () => {
    // print('loading')
    fetchData('2024-8-2','2024-8-9','2024-8-8','25000',option='put',timeframe="5minute",stock_code="NIFTY");
    // print('fetchaction')
    // loadWatchlist();
});

// Handle data fetching on button click
document.getElementById('fetchData').addEventListener('click', () => {
    console.log('fetching')
    const script_code = document.getElementById('symbol').value;
    const timeframe = document.getElementById('timeframe').value;
    const from_date = document.getElementById('fromdate').value;
    const to_date = document.getElementById('todate').value;
    const expiry_date = document.getElementById('expiry').value;
    const strike_price = document.getElementById('strike').value;
    const option = document.getElementById('option').value;
    
    fetchData(from_date,to_date,expiry_date,strike_price,option,timeframe,script_code);
});



