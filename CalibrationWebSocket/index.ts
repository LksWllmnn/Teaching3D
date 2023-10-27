import { WebSocket } from "ws";
import { BaseExpressRoute } from "./athaeck-websocket-express-base/athaeck-express-base/base/express";
import { BaseWebSocketExpressAdoon } from "./athaeck-websocket-express-base/base";
import { WebSocketHooks } from "./athaeck-websocket-express-base/base/hooks";
import { Free3DCalibrationData } from "./src/data/Free3DCalibrationData";
import { Free3DHooks } from "./src/hooks/Free3DHooks";
import { Free3DSocketListenerFactory } from "./src";
import bodyParser from "body-parser"



export class Free3DWebSocketServer extends BaseWebSocketExpressAdoon{
    private _free3DData: Free3DCalibrationData
    private _free3DHooks: Free3DHooks

    constructor(port:number){
        super(port)
        this.factory = new Free3DSocketListenerFactory("./listener/")
        this.initializeMiddleware()
        this._free3DData = new Free3DCalibrationData()
        this._free3DHooks = new Free3DHooks()
    }

    public get Free3DData(){
        return this._free3DData
    }
    public get Free3DHooks(){
        return this._free3DHooks
    }

    Init(webSocket: WebSocket, hooks: WebSocketHooks): void {
        
    }
    Disconnect(webSocket: WebSocket): WebSocketHooks | undefined {



        return undefined
        
    }
    AddRoute(route: BaseExpressRoute): void {
        
    }
    initializeMiddleware(): void {
        this.app.use(bodyParser.json());
    }
    
}

export const Free3DWebSocket = new Free3DWebSocketServer(8081)
Free3DWebSocket.Start()