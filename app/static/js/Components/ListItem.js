
import React, { Component } from 'react';

class ListItem extends Component{
    constructor(){
        super();
    }
    render() {
        let item = this.props.item;
        let claim = null;
        if(!item.purchaser_id){
            claim = (<button onClick={item.claim_handler}>
                Claim
                </button>);
        }
        else if(item.purchaser_id == user_id){
            claim = (<button onClick={item.unclaim_handler}>
                Unclaim
                </button>);
        }
        else{
            claim = <p>Item is already claimed</p>
        }
        return (
            <tr className="ListItem">
                <td>{ item.item_name }</td>
                <td>{ item.description }</td>
                <td>{ claim }</td>
            </tr>
        );
    }
}

export default ListItem;