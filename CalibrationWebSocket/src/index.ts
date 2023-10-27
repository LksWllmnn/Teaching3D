import { WebSocketListenerFactory } from "../athaeck-websocket-express-base/base";
import { StandardWebSocketDistributor } from "../athaeck-websocket-express-base/base/helper";
import config from "config"





export class Free3DSocketListenerFactory extends WebSocketListenerFactory{
    constructor(root:string){
        super(root)
    }
    protected TakeListener(): void {
        const listener:any[] = [
            StandardWebSocketDistributor
        ]

        const refs: string[] = config.get("listener") as string[]
        for(const ref of refs){
            const listenerRef = require(`${this.rootFolder + ref}`)
            if(!listenerRef){
                break;
            }
            listener.push(listenerRef)
        }

        this.AddListener(listener)
    }
}