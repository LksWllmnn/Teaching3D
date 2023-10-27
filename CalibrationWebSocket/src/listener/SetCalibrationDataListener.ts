import  WebSocket  from "ws";
import { BaseWebSocketExpressAdoon, BaseWebSocketListener } from "../../athaeck-websocket-express-base/base";
import { WebSocketHooks } from "../../athaeck-websocket-express-base/base/hooks";
import { Free3DWebSocketServer } from "../..";
import { CalibrationData, Free3DWebSocketEvents } from "../../types";




class SetCalibrationDataListener extends BaseWebSocketListener {
    listenerKey: string;
    private _application: Free3DWebSocketServer

    constructor(webSocketServer: BaseWebSocketExpressAdoon, webSocket: WebSocket.WebSocket, hooks: WebSocketHooks) {
        super(webSocketServer, webSocket, hooks)
        this._application = <Free3DWebSocketServer>webSocketServer
    }

    protected Init(): void {
        
    }
    protected SetKey(): void {
        this.listenerKey = Free3DWebSocketEvents.SET_CALIBRATION
    }
    public OnDisconnection(webSocket: WebSocket, hooks: WebSocketHooks): void {
        
    }
    protected listener(body: any): void {
        const data:CalibrationData = <CalibrationData>body

        this._application.Free3DData.SetId(data.id)
        this._application.Free3DHooks.DispatchHook(Free3DWebSocketEvents.UPDATE_CALIBRATION,this._application.Free3DData)
    }
}
module.exports = SetCalibrationDataListener