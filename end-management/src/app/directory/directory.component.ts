import { Component, OnInit } from '@angular/core';
import { LoggingService } from '../logging.service';
import { DataService } from '../data.service';

declare var firebase:any;

@Component({
  selector: 'app-directory',
  templateUrl: './directory.component.html',
  styleUrls: ['./directory.component.css']
})
export class DirectoryComponent implements OnInit {

  people = [];

  constructor(private logger: LoggingService,private dataService: DataService) {
  }

  ngOnInit() {
    // this.dataService.fetchData().subscribe(
    //   (data) => this.people = data
    // );

    this.fbGetData();
  }

  // 连接数据库并获取数据
  fbGetData() {
    // localhost:4200/directory
    firebase.database().ref('/').on('child_added',(snapshot) => {
      this.people.push(snapshot.val());
    });
  }

  // 向数据库传入数据
  fbPostData(name,color,phone) {
    firebase.database().ref('/').push({name:name,color:color,phone:phone});
  }

}
