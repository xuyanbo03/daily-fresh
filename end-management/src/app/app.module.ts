import { BrowserModule } from '@angular/platform-browser';
import { NgModule } from '@angular/core';
import { FormsModule } from '@angular/forms';
import { HttpModule } from '@angular/http';
import {HttpClientModule} from '@angular/common/http';

import { AngularFireModule } from 'angularfire2';

import { AppComponent } from './app.component';
import { NavbarComponent } from './navbar/navbar.component';
import { HomeComponent } from './home/home.component';
import { DirectoryComponent } from './directory/directory.component';

import { routing } from './app.routes';
import { FilterPipe } from './filter.pipe';
import { LoggingService } from './logging.service';
import { DataService } from './data.service';

@NgModule({
  declarations: [
    AppComponent,
    NavbarComponent,
    HomeComponent,
    DirectoryComponent,
    FilterPipe
  ],
  imports: [
    BrowserModule,
    routing,
    FormsModule,
    HttpModule,
    HttpClientModule,
    AngularFireModule
  ],
  providers: [LoggingService,DataService],
  bootstrap: [AppComponent]
})
export class AppModule { }
