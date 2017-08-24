import { Injectable } from '@angular/core';
import { Http } from '@angular/http';
import 'rxjs/add/operator/map';

@Injectable()
export class DataService {

  constructor(private http:Http) { }

  // 请求本地数据,处理对应数据
  fetchData() {
    return this.http.get('https://ng-management-8da57.firebaseio.com/.json')
      .map((res) => res.json());
  }

}
