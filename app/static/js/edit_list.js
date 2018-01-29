import React, { Component } from 'react';
import ReactDOM from 'react-dom';

import ItemList from './Components/ItemList'

  class App extends Component{
    constructor() {
        super();
        this.state = {list: []}
    }
    render() {
      return (<div className="ItemList">
                <ItemList items={this.state.list}/>
            </div>);
    }

    componentWillMount(){
        this.refreshList();
    }

    getClaimHandler(itemId, isUnclaim){
        let that = this;
        return function(){
            let claim = isUnclaim ? false : true;
            fetch('/claim_item/' + itemId,
            {method: 'POST',
            headers: new Headers({
                'Content-Type': 'application/json'
            }),
            credentials: 'include',
            body: JSON.stringify({'claim': claim})}
            ).then(function(response){
            console.log("In AJAX response")
            response.json().then(function(data){
                console.log(data)
                that.refreshList()
            },
            function(err){console.error("Failed to parse JSON")}
            )},
            function(err){
                console.log("Error: ")
                that.refreshList()
            })
        }
    };

    refreshList(){
    let that = this;
        fetch('/list_items/' + list_id,
        {method: 'GET',
        headers: new Headers({
            'Content-Type': 'application/json'
        }),
        credentials: 'include'}
        ).then(function(response){
        console.log("In list_items response")
        response.json().then(function(data){
            console.log(data);
            let len = data.items.length;
            for(let i = 0; i < len; i++){
                console.log(data.items[i]);
                data.items[i].claim_handler = that.getClaimHandler(data.items[i].list_item_id);
                data.items[i].unclaim_handler = that.getClaimHandler(data.items[i].list_item_id, true);
            }
            that.setState({list: data.items})
        },
        function(err){
            console.error("Failed to parse JSON");
            that.setState({list: []})}
        )},
        function(err){
            console.log("Error: ");
            that.setState({list: []})
        });
    }
  }




  ReactDOM.render(
    React.createElement(App, null),
    document.getElementById('list_container')
  );