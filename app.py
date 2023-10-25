from flask import Flask, jsonify, request
from ariadne import QueryType, load_schema_from_path, make_executable_schema
from graphql_server.flask import GraphQLView

app = Flask(__name__)

stocks_data = [
    {
        'name': 'STOCK01',
        'price': 20.30,
        'ticker': 'STAB'
    },
    {
        'name': 'STOCK02',
        'price': 130.00,
        'ticker': 'NMRT'
    }
]

ticker_data = [
    {
        'ticker': 'STOCK01',
        'historical_price_data': [23.45, 754.6, 45.67],
        'highest_price': 754.6,
        'lowest_price': 20.30,
        'trading_volume': 5304 
    },
        {
        'ticker': 'NMRT',
        'historical_price_data': [22.45, 29.6, 34.67],
        'highest_price': 130.00,
        'lowest_price': 22.45,
        'trading_volume': 9404 
    },
]

# GraphQL related code
ql_query = QueryType()
ql_schema_def = load_schema_from_path("schema.graphql")

# home route
@app.route('/', methods=['GET'])
def home_route():
    return jsonify("Hello to the home route for CST8916-Remote Data, Assignment 1")

# get all stocks
@app.route('/stock', methods=['GET'])
def stocks_route():
    return jsonify(stocks_data)

# edit the price of a stock
@app.route('/stock', methods=['PUT'])
def update_stock():
    for t in stocks_data:
        if t['ticker'] == request.json['ticker']:
            updated_price = request.json['price']
            t['price'] = updated_price
            return jsonify({'Msg': f'Updated stock price: ticker: {t["ticker"]} price: {updated_price}'})
    
    return jsonify({'Msg: Error ticker not found!'})



# post route, create stock
@app.route('/stock', methods=['POST'])
def create_stock():
    new_stock = {
        'name': request.json['name'],
        'price': request.json['price'],
        'ticker': request.json['ticker']
    }
    stocks_data.append(new_stock)
    return jsonify({'Msg': f'Stock created successfully {new_stock}'})

# delete a stock
@app.route('/stock', methods=['DELETE'])
def delete_stock():
    for i in stocks_data:
        if i['name'] == request.json['name']:
            stocks_data.remove(i)
            return jsonify({"Msg": "Stock deleted successfully!"})

@ql_query.field("stock")
def resolve_get_stock(*_, name):
    for i in stocks_data:
        if i['name'] == name:
            return i

@ql_query.field("stocks")
def resolve_get_stocks(*_):
    return stocks_data

@ql_query.field("tickerData")
def resolve_get_detailedData(_, info, ticker):
    for i in ticker_data:
        if i['ticker'] == ticker:
            return i 
        
ql_schema_def = make_executable_schema(ql_schema_def, ql_query)
app.add_url_rule('/graphql', view_func=GraphQLView.as_view('graphql', schema=ql_schema_def, graphql=True))

if __name__ == '__main__':
    app.run(port=5000)