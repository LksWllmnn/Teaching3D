import WebSocket from "ws";
import { BaseWebSocketExpressAdoon, BaseWebSocketListener } from "../../athaeck-websocket-express-base/base";
import { WebSocketHooks } from "../../athaeck-websocket-express-base/base/hooks";
import { Free3DWebSocketEvents } from "../../types";
import { Free3DWebSocketServer } from "../..";
import { Free3DCalibrationData } from "../data/Free3DCalibrationData";
import { ReceivedEvent } from "../../athaeck-websocket-express-base/base/helper";





class GetCalibrationDataListener extends BaseWebSocketListener {
    listenerKey: string;
    private _application: Free3DWebSocketServer

    constructor(webSocketServer: BaseWebSocketExpressAdoon, webSocket: WebSocket.WebSocket, hooks: WebSocketHooks) {
        super(webSocketServer, webSocket, hooks)
        this._application = <Free3DWebSocketServer>webSocketServer
    }

    protected Init(): void {
        this._application.Free3DHooks.SubscribeHookListener(Free3DWebSocketEvents.UPDATE_CALIBRATION, this.OnUpdateCalibration.bind(this))
    }
    protected SetKey(): void {
        this.listenerKey = Free3DWebSocketEvents.GET_CALIBRATION
    }
    public OnDisconnection(webSocket: WebSocket, hooks: WebSocketHooks): void {
        this._application.Free3DHooks.UnSubscribeListener(Free3DWebSocketEvents.UPDATE_CALIBRATION, this.OnUpdateCalibration.bind(this))
    }
    protected listener(body: any): void {
        if(this._application.Free3DData.GetId() === undefined){
            return
        }

        const response:ReceivedEvent = new ReceivedEvent(Free3DWebSocketEvents.On_UPDATE_CALIBRATION)
        response.addData("CALIBRATION",this._application.Free3DData)
        this.webSocket.send(response.JSONString)
    }

    private OnUpdateCalibration(data: Free3DCalibrationData) {
        const response: ReceivedEvent = new ReceivedEvent(Free3DWebSocketEvents.On_UPDATE_CALIBRATION)
        response.addData("CALIBRATION", data)
        this.webSocket.send(response.JSONString)
    }

}

module.exports = GetCalibrationDataListener